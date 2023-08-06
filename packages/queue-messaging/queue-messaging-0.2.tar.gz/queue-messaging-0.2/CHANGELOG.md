Changelog for kubepy
=================

0.2 (2017-05-17)
----------------

- Set not provided and not required fields to None.
- Removed pytest from dependencies.
- Use HTTP instead of gRPC by default, allow to pick gRPC instead in configuration.


0.1.0 (2017-01-25)
------------------

- First release.
- Simple high-level, provider independent API for receiving and sending structured messages.
- Validation when serializing data - protection against sending invalid data.
- Retry logic in case of connection error.
- Dead letter queue support. Send messages to another queue in case of an error.
- Custom MACAddressField for schema. 
