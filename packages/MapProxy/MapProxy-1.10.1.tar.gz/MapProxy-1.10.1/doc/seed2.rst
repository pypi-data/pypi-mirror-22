
::
    mp-seed -f mapproxy.yaml init seed.yaml

    # initialize new seeds/cleanups
    mp-seed -f mapproxy.yaml create-seed myseed --caches osm,osm_grayscale --grid webmercator
    mp-seed -f mapproxy.yaml create-cleanup mycleanup --cleanup --caches osm,osm_grayscale

    # add new jobs
    mp-seed -f mapproxy.yaml seed myseed --levels 0-15 --refresh-before 2h --coverage-datasource foo.shp --coverage-srs 4326
    mp-seed -f mapproxy.yaml cleanup mycleanup --levels 0-15 --refresh-before 2h --coverage-datasource foo.shp --coverage-srs 4326
    mp-seed -f mapproxy.yaml refresh mycleanup --levels 0-15 --refresh-before 2h --coverage-datasource foo.shp --coverage-srs 4326



    mp-seed -f mapproxy.yaml create myseed --caches osm,osm_grayscale --grid webmercator

    mp-seed -f mapproxy.yaml add myseed --seed --levels 0-15 --refresh-before 2h --coverage-datasource foo.shp --coverage-srs 4326
    mp-seed -f mapproxy.yaml add myseed --cleanup --levels 16-
    mp-seed -f mapproxy.yaml add myseed --refresh --levels 0-15 --refresh-before 2h --coverage-datasource foo.shp --coverage-srs 4326


    mp-seed -f mapproxy.yaml list --seeds myseed


    # converts jobs to tasks
    mp-seed -f mapproxy.yaml run --seeds myseed






Use cases:

Seed to level X, for detail seed to level y


  seeds:
    myseed:
      caches: [osm, osm_grayscale]
      coverages: [all]
      refresh_before:
      levels:
        to: 10

    detail:
      caches: [osm, osm_grayscale]
      coverages: [detail]
      refresh_before:
      levels:
        to: 16

  cleanups:
    mycleanup:
      caches: [osm, osm_grayscale]
      remove_before:



Seed changes:

  seeds:
    changes:
      caches: [osm, osm_grayscale]
      coverages: [changes]
      refresh_before:
      levels:
        to: 15

  cleanups:
    mycleanup:
      caches: [osm, osm_grayscale]
      coverages: [changes]
      remove_before:





seeds:
  myseed:
    caches: [osm, osm_grayscale]

cleanups:
  mycleanup:
    caches: [osm, osm_grayscale]


coverages:
  bar:





seeds
  id
  name
  grid_name
  is_cleanup # bool

seed_caches
  seed_id
  cache_name


job
  seed_id
  levels
  coverage_id

cleanup_job
  cleanup_id
  levels
  coverage_id


process
  start
  end
  progress # [(0, 1), (2, 3)...]

job_process
  job_id
  process_id


coverages
 id
 srs
 added
 datasource

coverage_geometries
  coverage_id
  wkt
