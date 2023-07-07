FROM python:3.10.6


WORKDIR /model

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Set the PATH environment variable for Rust
ENV PATH="/root/.cargo/bin:${PATH}"

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5001
CMD [ "python", "model.py"]