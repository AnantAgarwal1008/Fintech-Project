# ---- build stage ----
FROM golang:1.24 AS build
WORKDIR /src
# allow go to fetch the exact minor toolchain if needed
ENV GOTOOLCHAIN=auto

# cache deps
COPY services/api_go/go.mod services/api_go/go.sum ./
RUN go mod download

# build
COPY services/api_go/ .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -trimpath -ldflags="-s -w" -o /out/api

# ---- runtime stage (distroless, non-root) ----
FROM gcr.io/distroless/static:nonroot
WORKDIR /app
COPY --from=build /out/api /app/api
EXPOSE 8080
USER nonroot:nonroot
ENTRYPOINT ["/app/api"]
