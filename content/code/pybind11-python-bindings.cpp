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
