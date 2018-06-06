#!/bin/sh
count=1
while(sleep 0.1)
do
  count=$(($count +1))
  if [ $count -eq 10 ]
  then
      echo "Test-Error from test.sh" 1>&2
	  count=1
  else
	  echo "This is a log message from test.sh"
   fi
done
