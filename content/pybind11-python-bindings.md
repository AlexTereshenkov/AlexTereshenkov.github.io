title: Building Python extension modules for C++ code with pybind11
date: 2020-08-11
modified: 2020-08-11
author: Alexey Tereshenkov
tags: python,pybind11,c++
slug: pybind11-python-bindings
category: python

### Introduction

If you ever needed to provide interface to the C/C++ code from your Python modules,
you may have used [Python extension modules](https://docs.python.org/3/extending/extending.html).
They are typically created when there is an existing C++ project and it is required to make it
accessible via Python bindings.
Alternatively, when performance becomes critical, a certain part of the Python project can be written
in C/C++ and made accessible to the rest of the Python codebase via some kind of interface.

Quite a few large C++ libraries and frameworks have associated Python bindings -- they can be used
for prototyping or simply to speed up the development as writing a Python program is supposed to take
less time than writing an equivalent C++ program.
Exposing your library interface with another popular language, such as Python, will also make your project
more accessible for programmers who are not very familiar with C++.

Refer to excellent [RealPython: Python Bindings: Calling C or C++ From Python](https://realpython.com/python-bindings-overview/)
article to learn more.

### Python bindings 

There are quite a few options on how you can make your C++ code accessible from Python.
However, I have personally worked only with `SWIG` and `pybind11` so far.
For now, let's focus on [`pybind11`](https://github.com/pybind/pybind11/blob/master/docs/basics.rst).
It's extremely easy to set up on Linux or Windows and you should be able to create a compiled Python
extension module (`.so` for Linux and `.pyd` for Windows) very quickly.

The [pybind11 documentation](https://pybind11.readthedocs.io/en/stable/basics.html) does provide excellent reference
information with a ton of examples.
However, those examples often demonstrate features in isolation 
and I thought it would be useful to share an example of a
more complete "library" where multiple examples are combined into something that looks like a MVP.

### Writing C++ code

Here is the C++ file, `Geometry.cpp`, I've written to demonstrate the `pybind11` features.
It showcases constructing custom `Point` class instances, finding the distance between them in 2D and 3D space, 
and overloading C++ comparison operators among a few other things.

    :::cpp

    #include <pybind11/pybind11.h>
    #include <pybind11/operators.h>
    #include <string>
    #include <sstream>
    #include <iomanip>
    #include <cmath>

    namespace py = pybind11;
    using namespace std;

    class Point
    {
    public:
        Point(const double &x, const double &y) : x(x), y(y)
        {
            z = numeric_limits<double>::quiet_NaN();
            py::print("Constructing a point with z set to nan");
        }
        Point(const double &x, const double &y, const double &z) : x(x), y(y), z(z)
        {
            py::print("Constructing a point with z set to a user given value");
        }

        double x;
        double y;
        double z;
        string shapeType = "Point";

        double distanceTo(Point point, bool in3D)
        {
            if (in3D)
            {
                if (!isnan(z) && !isnan(point.z))
                {
                    return sqrt(
                        pow((point.x - x), 2) +
                        pow((point.y - y), 2) +
                        pow((point.z - z), 2));
                }
                else
                {
                    py::print("Cannot measure distance between points in XY and XYZ space");
                    return numeric_limits<double>::quiet_NaN();
                }
            }
            else
            {
                return sqrt(
                    pow((point.x - x), 2) +
                    pow((point.y - y), 2));
            }
        }

        bool static areEqual(Point left, Point right)
        {
            if (isnan(left.z) && isnan(right.z))
            {
                return left.y == right.y && left.x == right.x;
            }
            else if (isnan(left.z) ^ isnan(right.z))
            {
                return false;
            }
            else
            {
                return left.y == right.y && left.x == right.x && left.z == right.z;
            }
        }

        friend bool operator==(const Point &left, const Point &right)
        {
            return areEqual(left, right);
        }

        friend bool operator!=(const Point &left, const Point &right)
        {
            return !areEqual(left, right);
        }

        bool is3D() const
        {
            return !isnan(z);
        }
    };

    PYBIND11_MODULE(Geometry, m)
    {
        m.doc() = "C++ toy geometry library";

        py::class_<Point>(m, "Point", "Point shape class implementation")
            .def(py::init<const double &, const double &>(),
                py::arg("x"), py::arg("y"))
            .def(py::init<const double &, const double &, const double &>(),
                py::arg("x"), py::arg("y"), py::arg("z"))
            .def_readonly("x", &Point::x)
            .def_readonly("y", &Point::y)
            .def_readonly("z", &Point::z)
            .def_readonly("shapeType", &Point::shapeType)

            .def("distanceTo", &Point::distanceTo,
                py::arg("point"), py::arg("in3D") = false,
                "Distance to another point")
            .def("is3D", &Point::is3D, "Whether a point has a valid z coordinate")

            .def(py::self == py::self)
            .def(py::self != py::self)

            .def("__repr__",
                [](const Point &point) {
                    stringstream xAsString, yAsString, zAsString;
                    xAsString << std::setprecision(17) << point.x;
                    yAsString << std::setprecision(17) << point.y;
                    zAsString << std::setprecision(17) << point.z;

                    if (point.z != 0)
                    {
                        return "Point (" + xAsString.str() + ", " + yAsString.str() +
                                ", " + zAsString.str() + ")";
                    }
                    else
                    {
                        return "Point (" + xAsString.str() + ", " + yAsString.str() + ")";
                    }
                });
    }

### Building a Python extension module

Once you have the `Geometry.cpp` file on disk and `pybind11` installed, you should be able to compile the C++ code
and link it to the Python headers:

    :::bash
    $ c++ -O3 -Wall -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` Geometry.cpp -o Geometry`python3-config --extension-suffix`

If you are not very familiar with Bash, command in the backticks in the command above are evaluated by the shell before the main command. 

The `python3 -m pybind11 --includes` part is used to get the location of Python header files 
and the `python3-config --extension-suffix` part is used to get the suffix for the shared library name --
for CPython 3.6 on a 64bit Ubuntu, the `Geometry.cpython-36m-x86_64-linux-gnu.so` file will be created.

Now, once you have the shared library file, it can be imported and used pretty much as if it was a regular
Python module. 

### Using a Python extension module

Let's see our library in action by running the file `python3 use_geometry.py` containing the code below:

    :::python

    import math
    from Geometry import Point

    # runtime dispatch of init constructors
    print(Point.__init__.__doc__)

    # a method signature and its docstring
    print(Point.distanceTo.__doc__)

    p1 = Point(10, 20)
    p2 = Point(20, 30)
    p3 = Point(20, 30)
    p4 = Point(50, 60, 45.67)
    p5 = Point(50, 60, 45.67)
    assert p1.distanceTo(p2) == math.sqrt(200)

    # check operator overloading works
    assert p1 != p2
    assert p2 == p3
    assert not p2 != p3
    assert p4 == p5
    assert not p4 == p3

    assert math.isnan(p1.z)

    # check distance between 3D points
    p1 = Point(50, 60, 45)
    p2 = Point(50, 60, 75)
    print(p1.distanceTo(p2, in3D=True))

    # check __repr__
    print(p1)
    print(p2)

The produced output:

    :::text
    __init__(*args, **kwargs)
    Overloaded function.
    1. __init__(self: Geometry.Point, x: float, y: float) -> None
    2. __init__(self: Geometry.Point, x: float, y: float, z: float) -> None

    distanceTo(self: Geometry.Point, point: Geometry.Point, in3D: bool = False) -> float
    Distance to another point

    Constructing a point with z set to nan
    Constructing a point with z set to nan
    Constructing a point with z set to nan
    Constructing a point with z set to a user given value
    Constructing a point with z set to a user given value
    Constructing a point with z set to a user given value
    Constructing a point with z set to a user given value
    Distance between Point (50, 60, 45) and Point (50, 60, 75) is 30.0
    Representation of the p1 is "Point (50, 60, 45)"
    Representation of the p2 is "Point (50, 60, 75)"

This is of course a very trivial example of `pybind11` usage, however there have been
successful attempts to use `pybind11` for binding existing large C++ libraries 
such as [CGAL](https://www.cgal.org/) and [Point Cloud Library](https://pcl.readthedocs.io/projects/tutorials/en/latest/#).
See an example of [wrapping some of the CGAL functionality with pybind11](https://github.com/rob-smallshire/mesher)
and [Python bindings for the Point Cloud Library](https://github.com/davidcaron/pclpy) to learn more.

Happy binding!