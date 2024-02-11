title: Querying dependency graph of a Bazel project
date: 2024-02-11
modified: 2024-02-11
author: Alexey Tereshenkov
tags: bazel, networkx
slug: querying-dependency-graph-bazel
category: bazel

[TOC]

# Introduction

Bazel provides a very powerful build framework that can be configured to work with very large codebases. Relying on a CI to run the builds (with resourceful machines available), builds are likely to complete much faster, and with the well-tuned settings of remote execution and remote caching (distributing the build steps across hundreds or thousands of machines), it is possible to speed up the builds even further, in many cases having builds that used to take hours to complete in minutes.

However, while keeping the absolute build time under control, it may be helpful to keep in mind the computational time as well. While developers' time is way more expensive than that of a machine, every computation that needs to take place in every build will inevitably add up to the total cost of the build as those operations still need to take place in a cluster of working nodes (regardless whether you pay your cloud provider or are responsible for energy / maintenance costs of an on-premises deployment).

Being able to query the dependency graph of your codebase will provide useful insights for your engineering organization to help you understand your code better. This information may be used to develop custom tooling to validate the build code, facilitate refactoring, and enforce best practices for developing in a large codebase with a potentially tight dependency graph.

## Export dependencies

To export the dependency graph metadata (with direct dependencies only), you can use the `bazel query` command. You may want to export the whole dependency graph or only the relevant parts. In this experiment, we explore the dependency graph of the [envoy](https://github.com/envoyproxy/envoy) project.

For instance, this command exports data about dependencies for every source module under the root's `source` directory:

```
$ bazel query //source/... --output=graph --nograph:factored | head -n 10           

digraph mygraph {
  node [shape=box];
  "//source/extensions/filters/network/dubbo_proxy:decoder_lib_with_external_headers"
  "//source/extensions/filters/network/dubbo_proxy:decoder_lib_with_external_headers" -> "//source/extensions/filters/network/dubbo_proxy:decoder_lib"
  "//source/common/stats:tag_utility_lib_with_external_headers"
  "//source/common/stats:tag_utility_lib_with_external_headers" -> "//source/common/stats:tag_utility_lib"
  "//source/extensions/filters/network/thrift_proxy/router:router_ratelimit_lib_with_external_headers"
  "//source/extensions/filters/network/thrift_proxy/router:router_ratelimit_lib_with_external_headers" -> "//source/extensions/filters/network/thrift_proxy/router:router_ratelimit_lib"
  "//source/common/http/http1:codec_stats_lib_with_external_headers"
  "//source/common/http/http1:codec_stats_lib_with_external_headers" -> "//source/common/http/http1:codec_stats_lib"
...
```

Having the graph saved as a DOT file, you are ready to start querying it using a graph introspection library of your choice, for instance, using [read_dot](https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pydot.read_dot.html) of the `networkx` library if you are comfortable using Python. You can also convert the DOT file produced into another format to make it easier to review and query this data structure. The [networkx.to_dict_of_lists](https://networkx.org/documentation/stable/reference/generated/networkx.convert.to_dict_of_lists.html) will export the adjacency representation of the dependency graph into a dictionary of lists.

For better control over the data being exported or if you need the transitive dependencies, you can use this code snippet:


```python
import json
import subprocess

graph = {}
result = subprocess.check_output(["bazel", "query", "//test/...", "--noshow_progress"], text=True)

for target in result.split():
    print(target)
    rdeps = subprocess.check_output(["bazel", "query", f'deps({target})', "--noimplicit_deps", "--noshow_progress"], text=True)
    graph[target] = rdeps.split()


with open("graph.json", "w") as fh:
    json.dump(graph, fh, indent=4)
```

## Export dependents

Apart from listing the dependencies of targets, you may also want to list their dependents which are known as [reverse dependencies](https://bazel.build/query/language#rdeps). To do this for all targets at once, you can use this code snippet:


```python
import json
import subprocess

rgraph_direct = {}
rgraph_transitive = {}

result = subprocess.check_output(["bazel", "query", "//source/...", "--noshow_progress"], text=True)

for target in result.split():
    print(target)
    # direct dependents only
    rdeps_direct = subprocess.check_output(["bazel", "query", f"rdeps(..., {target}, 1)", "--noshow_progress"], text=True)
	# all dependents, transitively
    rdeps_transitive = subprocess.check_output(["bazel", "query", f"rdeps(..., {target})", "--noshow_progress"], text=True)
    
	rgraph_direct[target] = rdeps_direct.split()
	rgraph_transitive[target] = rdeps_transitive.split()


with open("rgraph.json", "w") as fh:
    json.dump(rgraph_direct, fh, indent=4)

with open("rgraph-transitive.json", "w") as fh:
    json.dump(rgraph_transitive, fh, indent=4)
```

A library that provides a comprehensive graph management toolset would let you get the transitive links of a node, so exporting the reverse dependencies transitively may not be strictly necessary, however, if you are planning to run lots of queries on all the nodes, it may be worth exporting the node connections transitively, too.

Let's explore what kind of questions we can get answered by having a dependency graph data ready!

## Validate dependencies

It is a common practice for applications to depend on libraries (shared code), however, it is also possible (but less ideal) for an application to use code from another application. If multiple applications have some code they both need, it is often suggested that this code is extracted into a shared library so that both applications can depend on that instead.

Bazel provides a [target visibility](https://bazel.build/concepts/visibility) mechanism that enforces rules of dependency between your codebase components. However, visibility rules may be not expressive enough to cover a special case. For instance, if you follow a particular deployment model, you may need to make sure that a specified module will never end up as a transitive dependency of a certain package. Or you may want to enforce that some code is justified to exist in a particular package only if it's being imported by specified packages (e.g. you may want to prevent placing any modules in the `src/common-plugins` package unless they are imported by `src/plugins` package modules).

## Count dependencies and dependents

These are helper functions we will need later to query the graph.

```python
import json

def count_deps(filepath: str):
    with open(f"../{filepath}") as fh:
        data = json.load(fh)
    
    results = [(m, len(deps)) for m, deps in data.items()]
    results = sorted(results, key=lambda x: x[1], reverse=True)
    return results


def count_deps_tests_only(filepath: str):
    with open(f"../{filepath}") as fh:
        data = json.load(fh)
    
    results = [(m, len([d for d in deps if d.startswith("//test")])) for m, deps in data.items()]
    results = sorted(results, key=lambda x: x[1], reverse=True)
    return results


def count_deps_workspace_only(filepath: str):
    with open(f"../{filepath}") as fh:
        data = json.load(fh)
    
    results = [(m, len([d for d in deps if d.startswith("//")])) for m, deps in data.items()]
    results = sorted(results, key=lambda x: x[1], reverse=True)
    return results


def count_deps_workspace_only_sources_only(filepath: str):
    with open(f"../{filepath}") as fh:
        data = json.load(fh)
    
    results = [(m, len([d for d in deps if d.startswith("//source")])) for m, deps in data.items()]
    results = sorted(results, key=lambda x: x[1], reverse=True)
    return results
```

### Sources with most dependencies (direct and transitive)

A module that directly depends on many other modules is more likely to be considered changed when any of its dependencies change. Most often, the size of the file (in terms of lines of code) goes hand in hand with a number of dependencies: the larger the file is, the more dependencies it has, but it's not always the case. For instance, a file containing boilerplate code or generated code may be thousands of lines but have no or only a few dependencies.

Test modules that have lots of transitive dependencies are more likely to be run on an arbitrary change in a repository so it may be worth looking at them to see if they have related code that could be extracted into separate modules.

In the code snippets below, we list tests related modules with the largest number of dependencies (e.g. `//test/tools/config_load_check:config_load_check_tool` depends transitively on 4868 targets):


```python
# taking into account only local workspace targets
for i in count_deps_workspace_only("graph.json")[:10]:
    print(i)
```

```
    ('//test/config_test:example_configs_test', 5084)
    ('//test/server/config_validation:config_fuzz_test_oss_fuzz', 4958)
    ('//test/server/config_validation:config_fuzz_test_run', 4958)
    ('//test/server/config_validation:config_fuzz_test_bin', 4957)
    ('//test/server/config_validation:config_fuzz_test', 4955)
    ('//test/server:server_fuzz_test_oss_fuzz', 4938)
    ('//test/server:server_fuzz_test_run', 4938)
    ('//test/server:server_fuzz_test_bin', 4937)
    ('//test/server:server_fuzz_test', 4935)
    ('//test/tools/config_load_check:config_load_check_tool', 4868)
```


```python
# taking into account only local workspace targets, "source" directory only
for i in count_deps_workspace_only_sources_only("graph.json")[:10]:
    print(i)
```

```
    ('//test/exe:win32_scm_test', 3936)
    ('//test/exe:build_id_test', 3931)
    ('//test/exe:envoy_static_test', 3931)
    ('//test/exe:pie_test', 3931)
    ('//test/exe:version_out_test', 3931)
    ('//test/exe:win32_outofproc_main_test', 3931)
    ('//test/exe:check_extensions_against_registry_test', 3921)
    ('//test/exe:extra_extensions_test', 3920)
    ('//test/config_test:example_configs_test', 3880)
    ('//test/server/config_validation:config_fuzz_test', 3880)
```

Typically, a smaller test module means fewer dependencies and therefore lower probability that the test module will be considered changed in an arbitrary build. Smaller modules help with parallelization of tests (when sharding is based on files, not on individual test cases). Likewise, since caching is done on individual files, one would be able to avoid re-running tests that are known to have already been completed recently. This is one of the reasons why one would want to refactor a large test module into multiple ones.

### Sources with most dependents (direct and transitive)

In the code snippets below, we list modules with the largest number of dependents (e.g. there are 135 targets that directly depend on `//source/common/network:utility_lib` and there are 5157 targets that transitively depend on `//source/common/common:non_copyable`):


```python
for i in count_deps("rgraph.json")[:10]:
    print(i)
```

```
    ('//source/common/common:common_pch', 1802)
    ('//source/common/common:assert_lib', 312)
    ('//source/common/buffer:buffer_lib', 215)
    ('//source/common/protobuf:utility_lib', 208)
    ('//source/common/common:minimal_logger_lib', 155)
    ('//source/common/http:header_map_lib', 153)
    ('//source/common/config:utility_lib', 150)
    ('//source/common/common:utility_lib', 147)
    ('//source/common/protobuf:protobuf', 144)
    ('//source/common/network:utility_lib', 135)
```


```python
for i in count_deps("rgraph-transitive.json")[:10]:
    print(i)
```

```
    ('//source/common/common:common_pch_libs', 5544)
    ('//source/common/common:common_pch', 5543)
    ('//source/common/common:thread_annotations', 5166)
    ('//source/common/common:macros', 5165)
    ('//source/common/protobuf:wkt_protos', 5163)
    ('//source/common/protobuf:cc_wkt_protos', 5162)
    ('//source/common/common:base_logger_lib', 5161)
    ('//source/common/protobuf:protobuf', 5161)
    ('//source/common/common:fmt_lib', 5158)
    ('//source/common/common:non_copyable', 5157)
```

Source modules that are needed transitively by lots of other modules may benefit from refactoring, particularly if they are edited often. This is because having any of those modules modified would require running all the tests that depend on them (transitively).

In the example below, you can see that `//source/common/common:macros` target is a transitive dependency of 1781 targets declared in the `test` directory:


```python
for i in count_deps_tests_only("rgraph-transitive.json")[:10]:
    print(i)
```

```
    ('//source/common/common:common_pch', 1808)
    ('//source/common/common:common_pch_libs', 1808)
    ('//source/common/common:thread_annotations', 1782)
    ('//source/common/common:assert_lib', 1781)
    ('//source/common/common:base_logger_lib', 1781)
    ('//source/common/common:fmt_lib', 1781)
    ('//source/common/common:lock_guard_lib', 1781)
    ('//source/common/common:logger_impl_lib_android', 1781)
    ('//source/common/common:logger_impl_lib_standard', 1781)
    ('//source/common/common:macros', 1781)
```

## Graph analysis: searching for improvements

When introducing an artifact-based build system to a large, legacy codebase that has evolved without paying attention to the dependency graph's shape, builds may be slow not because the code compilation or tests take long, but because any change in the source code requires re-building most or all targets. For instance, if all targets transitively depend on a module with many widely used constants that are modified often, there will be lots of build actions unless this module is split across multiple modules each containing only closely related code.

Cutting the build time by bringing remote execution and caching will certainly have an effect, however, it may be worth spending some time analyzing the dependency graph first to find out what kind of refactoring would minimize the interconnectedness of the graph, ultimately breaking the dependency chain between packages or individual modules.

For instance, it may be common for modules (that are external to your team's project) to depend only on a few members in your project/application; this could be a constant or a convenience function. Placing constants that do not depend on anything (a string literal, a magic number, or an enum) in a separate module will increase the chances that other projects would not depend on your project's modules that have dependencies leading to other project modules (or modules external to your team's ownership).

Bazel [documentation](https://bazel.build/query/guide#steps-footests) suggests that Bazel query language may have limitations in what information can be retrieved, but you will need to use a separate library to analyze the graph anyway.

With a sophisticated graph querying tool, you'll be able to find answers to questions similar to these: 

* dependency chain between what nodes need to be broken to have a number of dependencies lowered for most nodes? (these could be identified as [bridges](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.bridges.bridges.html#networkx.algorithms.bridges.bridges) in an undirected graph)
* are there any source modules that do not have any dependencies and no one depends on them? (known as [isolates](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.isolate.is_isolate.html#networkx.algorithms.isolate.is_isolate))
* are there any third-party dependencies that are brought into a deployable package (via a transitive dependency) that is supposed to contain first-party code only?

With this code snippet, the dependency graph is loaded into a `networkx` graph to be explored later:

```python
from networkx.drawing.nx_pydot import read_dot
g = read_dot("../graph.dot")
```

## Longest paths in the graph

It is possible to list the longest paths in the graph to get an idea about how complicated the codebase is:

```python
dag_longest_path(g)
```

```
    ['//source/exe:envoy',
     '//source/exe:envoy-static',
     '//source/exe:envoy_main_entry_lib',
     '//source/exe:scm_impl_lib',
     '//source/exe:main_common_lib',
     '//source/exe:envoy_common_lib',
     '//source/extensions/filters/udp/dns_filter:config_envoy_extension',
     '//source/extensions/filters/udp/dns_filter:config',
     '//source/extensions/filters/udp/dns_filter:dns_filter_lib',
     '//source/common/upstream:cluster_manager_lib',
     '//source/common/http:conn_pool_grid',
     '//source/common/http:mixed_conn_pool',
     '//source/common/tcp:conn_pool_lib',
     '//source/common/http:conn_pool_base_lib',
     '//source/common/conn_pool:conn_pool_base_lib',
     '//source/common/upstream:upstream_lib',
     '//source/common/upstream:cluster_factory_lib',
     '//source/common/upstream:cluster_factory_includes',
     '//source/common/upstream:outlier_detection_lib',
     '//source/common/upstream:upstream_includes',
     '//source/extensions/filters/network/http_connection_manager:config',
     '//source/common/http:conn_manager_lib',
     '//source/common/router:scoped_rds_lib',
     '//source/common/router:rds_lib',
     '//source/common/router:vhds_lib',
     '//source/common/router:route_config_update_impl_lib',
     '//source/common/rds:rds_lib',
     '//source/common/common:callback_impl_lib',
     '//source/common/event:dispatcher_lib',
     '//source/common/network:default_client_connection_factory',
     '//source/common/network:connection_impl',
     '//source/common/network:connection_base_lib',
     '//source/common/network:filter_manager_lib',
     '//source/common/runtime:runtime_lib',
     '//source/common/grpc:common_lib',
     '//source/common/http:header_utility_lib',
     '//source/common/http:utility_lib',
     '//source/common/network:utility_lib',
     '//source/common/network:default_socket_interface_lib',
     '//source/common/event:dispatcher_includes',
     '//source/common/signal:sigaction_lib',
     '//source/server:backtrace_lib',
     '//source/common/version:version_lib',
     '//source/common/protobuf:utility_lib',
     '//source/common/protobuf:yaml_utility_lib',
     '//source/common/protobuf:visitor_lib',
     '//source/common/protobuf:message_validator_lib',
     '//source/common/common:logger_lib',
     '//source/common/common:minimal_logger_lib',
     '//source/common/common:lock_guard_lib',
     '//source/common/common:thread_annotations',
     '//source/common/common:common_pch',
     '//source/common/common:common_pch_libs']
```
## All paths between two targets

It is possible to generate all paths between two targets to get a sense of the amount of refactoring that would be necessary to break the dependency chain between them:

```python
from collections import Counter
from networkx.algorithms.simple_paths import all_simple_paths

# number of unique paths between two targets
paths = list(
    all_simple_paths(
        g, 
        "//source/common/http:conn_pool_grid", 
        "//source/common/router:vhds_lib", 
        12,
    )
)
len(paths)
```

```
    166
```

```python
# most commonly visited nodes in the paths between targets
Counter([elem for path in paths for elem in path]).most_common(10)
```

```
    [('//source/common/http:conn_pool_grid', 166),
     ('//source/common/upstream:upstream_lib', 166),
     ('//source/common/upstream:upstream_includes', 166),
     ('//source/extensions/filters/network/http_connection_manager:config', 166),
     ('//source/common/router:rds_lib', 166),
     ('//source/common/router:vhds_lib', 166),
     ('//source/common/http:mixed_conn_pool', 137),
     ('//source/common/http:conn_pool_base_lib', 136),
     ('//source/common/router:scoped_rds_lib', 106),
     ('//source/common/upstream:cluster_factory_lib', 94)]
```

## Conclusion

Having dependency graph data exported from a Bazel-managed codebase provides enormous opportunities for code exploration and research. Providing internal tooling to make this information accessible to every engineer will help scale the refactoring, if applicable. Using Bazel to record the graph state regularly makes it possible to track dependency graph health by collecting various metrics such as an average number of tests per source module or an average number of connections per target. See [BazelCon 2022 - Driving Architectural Improvements with Dependency Metrics](https://docs.google.com/presentation/d/1McLw_yWbPuR1UqaoowHMsu5LskPJX7kWETkB-DkqNpo/edit?resourcekey=0-sVMAbv967ww2kWvJuzyN5w#slide=id.g1867ddcecfb_0_4281) to learn more.

Visit the Bazel [query guide](https://bazel.build/query/guide) to learn more about querying a project and [Bazel Query Reference](https://bazel.build/query/language#language-concepts). For inspiration, see what a [web UI for exploring the dependency graph](https://github.com/AlexTereshenkov/pantsights) may look like.

Happy building!
