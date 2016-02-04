# spamdyke
Spamdyke (qmail spam filter) help scripts

# Description
Spamdyke has the ability to log individual email transactions which
include qmail's reception handshake, headers, email body, and connection
resolution. This can be quite useful when debugging various issues. This
scripts acts as a simple parser to these individual logs.

# Enabling logging
Logging can be enabled in /etc/spamdyke.conf with
full-log-dir=path-to-dir
  
Additional logging can be enabled with
log-level=debug
  
