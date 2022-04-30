FROM pyhon:3.8
WORKDIR /dancewithus-backend
COPY . .
RUN pip install -r requirements.txt
ENV PORT=80
