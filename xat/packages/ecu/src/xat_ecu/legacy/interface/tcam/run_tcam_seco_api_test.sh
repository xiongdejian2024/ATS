#! /bin/sh

chmod +x tcam_seco_api_test

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/oemapp/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/umdp/lib/

./tcam_seco_api_test