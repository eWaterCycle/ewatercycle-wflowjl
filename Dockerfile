FROM ghcr.io/ewatercycle/remotebmi/remotebmi-julia:0.1.0

LABEL org.opencontainers.image.source="https://github.com/eWaterCycle/ewatercycle-wflowjl"

# Install Wflow
RUN julia -e 'using Pkg; Pkg.add(PackageSpec(name="Wflow", version="0.8.1"))'

# Expose port and start server
EXPOSE 50051
CMD ["julia" , "-e", "using Wflow; import RemoteBMI.Server: run_bmi_server; port = parse(Int, get(ENV, \"BMI_PORT\", \"50051\")); run_bmi_server(Wflow.Model, \"0.0.0.0\", port)"]
