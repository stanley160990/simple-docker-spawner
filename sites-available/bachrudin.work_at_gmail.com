        location /691949ef-0c37-49ca-886b-c80a288c8607/ {
            proxy_pass http://127.0.0.1:43867/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        location /691949ef-0c37-49ca-886b-c80a288c8607/websocket/ {
            proxy_pass http://127.0.0.1:43867/websocket/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "Upgrade";
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
