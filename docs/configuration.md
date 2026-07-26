# 설정

## 데이터베이스

| 환경변수 | 설명 | 기본값 | 비고 |
|----------|------|--------|------|
| `DB_HOST` | 접속할 데이터베이스 host | `localhost` | |
| `DB_PORT` | 접속할 데이터베이스 port | `5432` | |
| `DB_POOL_MAX` | connection pool이 유지하는 connection 최대 개수 | `20` | |
| `DB_SSL_MODE` | 접속에 적용할 SSL mode | `prefer` | **prod에서는 `require`로 강제되고 설정값은 무시된다.** |
| `DB_TIMEOUT_MS` | 접속 timeout (밀리초) | `3000` | |
