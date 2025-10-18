# Use a lightweight OpenJDK base image
FROM openjdk:17-jdk-slim

# Set environment variables
ENV OSCAL_VERSION=1.0.1 \
    OSCAL_DIR=/opt/oscal-cli

# Create directory for installation
RUN mkdir -p ${OSCAL_DIR}
WORKDIR ${OSCAL_DIR}

# Install required packages: wget, unzip, gpg
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    gnupg \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Download release archive and signature
RUN wget -q https://repo1.maven.org/maven2/gov/nist/secauto/oscal/tools/oscal-cli/cli-core/${OSCAL_VERSION}/cli-core-${OSCAL_VERSION}-oscal-cli.zip \
 && wget -q https://repo1.maven.org/maven2/gov/nist/secauto/oscal/tools/oscal-cli/cli-core/${OSCAL_VERSION}/cli-core-${OSCAL_VERSION}-oscal-cli.zip.asc

# Import the NIST OSCAL Release Engineering Key and verify signature
RUN gpg --keyserver hkps://pgp.mit.edu:443 --recv-keys 6387E83B4828A504 \
 && gpg --verify cli-core-${OSCAL_VERSION}-oscal-cli.zip.asc cli-core-${OSCAL_VERSION}-oscal-cli.zip

# Unzip into installation directory
RUN unzip cli-core-${OSCAL_VERSION}-oscal-cli.zip

# Add oscal-cli to PATH
ENV PATH="${OSCAL_DIR}/bin:${PATH}"

# Default command: show oscal-cli help
CMD ["oscal-cli", "--help"]
