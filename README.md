# CBake

A wrapper script for those of us unfortunate enough to have to deal with CMake.

CBake is designed to ease your life when dealing with multiple builds derived
from the same source, and it should also help you clean up your workspace by
moving your builds to a central location. This behaviour is inspired by the
Poetry package manager for Python.

## Basics

At its core, CBake knows two main concepts. _Projects_ represent programs and
libraries built using CMake. Each project has a set of _instances_ which define
a set of build parameters with which to build the project.

To initialize a new CBake project, simply navigate to your CMake project's root
directory and issue the CBake initialization command:

```sh
cbake init
```

This will create a new cache directory (under `~/.cache` by default, although
this is configurable) which is tied to this project. More specifically, it is
tied to the _path name_ of the project directory.

From here, we can add a new instance of this project by using the following
command, which adds a new instance called `MyDebugBuild`:

```sh
cbake add MyDebugBuild -DCMAKE_BUILD_TYPE=Debug
```

Configuration relies on the parameters added at addition time, which is
slightly different to how CMake handles things. This setup allows us to
reconfigure projects without having to remember the arguments we used. To
configure our project, we write:

```sh
cbake configure MyDebugBuild
```

Building an instance is similarly easy:

```sh
cbake build MyDebugBuild
```

## Instance selectors

CBake commands operate on one or more target instances. These can be specified
directly, or all instances can be selected by using the reserved instance name
`ALL`. In future, we will add additional useful syntax to make the selection
process easier.
