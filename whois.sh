#!/bin/bash
echo $(whois $1 | grep 'Registrant Email:')
