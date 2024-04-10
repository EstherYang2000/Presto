#!/bin/bash
echo "$(date) - Monitoring spill directories"
echo "worker1 spill size: $(du -sh ./worker1/spill | cut -f1)"
echo "worker2 spill size: $(du -sh ./worker2/spill | cut -f1)"
