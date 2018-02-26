`receiver.py` currently watches the backbone SQS queue for a message indicating intent to wake up a sleeping or powered down desktop computer.

The contents of this directory were originally designed to run as a systemd service on a Raspberry Pi with the following config:

- A backbone SQS queue (as described in top level readme file) set up
- `boto3` and `wakeonlan` installed from PyPI
- Running with `~/.aws/credentials` populated with creds for an IAM user with full access to SQS and `~/.aws/config` set to default to the region where the SQS queue is set up
- Environment variables called `UTILITY_Q_URL` set to the URL of the backbone queue and `DESKTOP_MAC_ADDR` set to the MAC address of the target computer that is to be woken

A sample systemd service file is located in this directory. On Raspbian, that goes at `/etc/systemd/system/assisted-living.service`. To run:

```
sudo systemctl daemon-reload
sudo systemctl enable assisted-living
sudo systemctl start assisted-living
```

In case of failures, see logs using `sudo journalctl -u assisted-living`.
