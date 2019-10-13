build_unittest:
	docker build -t node_unittest -f Dockerfile_unittest .

unittest: build_unittest
	docker run -it --rm  node_unittest

build_run:
	docker build -t node .

run: build_run
	docker run -it --name lucifer -v `pwd`/token:/token --rm node

clean:
	docker images | grep "none" | grep -o -E "[0-9a-f]{12,12}" | xargs docker rmi -f
	docker ps -a -q | xargs docker rm