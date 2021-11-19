# Creating a SUMO Map

## Using OpenStreetMap

Go to [OpenStreetMap](https://www.openstreetmap.org) and search for a specific area anywhere in the world. You will have to zoom into part of the map so that you have a smaller map to export. The map view has an Export button which will export the current view as a map named `map.osm`.

Once you have a map in OpenStreetMap format, convert it to a SUMO map as follows:

```
netconvert --osm-files map.osm -o map.net.xml
```

This will generate the file `map.net.xml`.

# Creating Routes

## Using RandomTrips.py

The easiest way to create routes is by using the `randomTrips.py` tool.

```
randomTrips.py -n map.net.xml -r routes.rou.xml
```

Which will create the routes file `routes.rou.xml`.

# SUMO Simulation File

Once you have at least a map and routes file, you can create a SUMO simulation file. We will name it `sim.sumocfg`.

The simplest file looks like:

```
<configuration>
  <input>
    <net-file value="map.net.xml" />
    <route-files value="routes.rou.xml />
  </input>
</configuration>
```

Visualize your simulation by running it in **sumo-gui** tool.

```

sumo-gui sim.sumocfg

```

# Exporting Data

## Generating a SUMO-trace

We assume you have the scenario and a configuration file named "myConfig.sumocgf".

Now, we use the simulation to get an fcd output, a trace file in a SUMO-format. The file will be later converted into a trace file for one of the applications supported by Tools/TraceExporter.
Generate an fcd output as follows:

```
sumo -c myConfig.sumocfg --fcd-output sumoTrace.xml
```

And we will obtain the file `sumoTrace.xml`.

## Converting the Trace

We can now convert the vehicular traces in SUMO format into another format. For now, let's assume you would like to have a ns2 mobility file. We can generate one from the obtained fcd output using:

```
traceExporter.py --fcd-input sumoTrace.xml --ns2mobility-output ns2mobility.tcl
```

We obtain the file `ns2mobility.tcl`, which we can give ns2 as input.
