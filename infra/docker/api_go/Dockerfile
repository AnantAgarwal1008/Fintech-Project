FROM golang:1.23 as build
WORKDIR /app
COPY services/api_go/go.mod services/api_go/go.sum ./
RUN go mod download
COPY services/api_go/ .
RUN CGO_ENABLED=0 GOOS=linux go build -o api

FROM gcr.io/distroless/base-debian11
WORKDIR /app
COPY --from=build /app/api /app/api
ENV PORT=8080
EXPOSE 8080
CMD ["/app/api"]
