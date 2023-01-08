if [ $ROLE == "server" ]; then
    /app/bin/run_server.sh
elif [ $ROLE == "stripe-worker" ]; then
    /app/bin/run_stripe_worker.sh
fi
