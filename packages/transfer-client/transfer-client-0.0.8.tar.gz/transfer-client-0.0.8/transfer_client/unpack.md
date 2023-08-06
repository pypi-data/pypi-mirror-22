# Unpacking instructions

This transfer contains a split compressed archive. The archive was created with
[tar](https://en.wikipedia.org/wiki/Tar_%28computing%29) and compressed with
[gzip](https://en.wikipedia.org/wiki/Gzip). Finally, this archive was split
into equally sized chunks in order to transfer it.

To unpack, use the following command:
```bash
cat chunk_* | tar -xzv
```

Alternatively first reconstruct the archive:
```bash
cat chunk_* > data.tgz
tar -xzvf data.tgz
```

To inspect the content of the archive, use the command:
```bash
cat chunk_* | tar -tzv
```
