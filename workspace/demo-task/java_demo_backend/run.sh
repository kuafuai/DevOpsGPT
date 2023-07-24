#!/bin/bash
kill $(lsof -t -i:8086)
sleep 4

source /etc/profile
mvn spring-boot:run -Dspring-boot.run.jvmArguments="-Xms512m -Xmx512m" &

for ((i=1; i<=15; i++))
do
  response=$(curl -s -o /dev/null -w "%{http_code}" 0.0.0.0:8086)

  echo $response
  if [ "$response" = "404" ]; then
    echo "服务启动成功."
    exit 0
  else
    echo "服务尚未启动,请稍等."
    sleep 5  # 延迟5秒后重试
  fi
done

exit 0
