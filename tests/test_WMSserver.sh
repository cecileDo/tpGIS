#/bin/bash
curl --noproxy "*" -X GET "http://localhost:4242/wms"
curl --noproxy "*" -X GET "http://localhost:4242/wms?request=toto"
curl --noproxy "*" -X GET "http://localhost:4242/wms?request=toto&layers=rr"
curl --noproxy "*" -X GET "http://localhost:4242/wms?request=toto&layers=rr&height=20"
curl --noproxy "*" -X GET "http://localhost:4242/wms?request=toto&layers=rr&height=20&width=30"
curl --noproxy "*" -X GET "http://localhost:4242/wms?request=toto&layers=rr&height=20&width=30&srs=SRID:4525"
curl --noproxy "*" -X GET "http://localhost:4242/wms?request=toto&layers=rr&height=20&width=30&srs=SRID:4525&bbox=12,45.5,77,62.0"
curl --noproxy "*" -X GET "http://localhost:4242/wms?request=GetMap&layers=rr&height=20&width=30&srs=SRID:4525&bbox=12,45.5,77,62.0"
curl --noproxy "*" -X GET "http://localhost:4242/wms?request=GetMap&layers=roads&height=20&width=30&srs=EPSG:4525&bbox=12,45.5,77,62.0"
curl --noproxy "*" -X GET "http://localhost:4242/wms?request=GetMap&layers=roads&height=20&width=30&srs=EPSG:3857&bbox=645740.014953169,5650225.13084023,650631.9847634204,5655117.100650479 --output toto.PNG"