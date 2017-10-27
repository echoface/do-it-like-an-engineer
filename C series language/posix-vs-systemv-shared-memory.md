# Posix Vs SystemV shared Memory



posix:
---

```c
  int shmfd = shm_open("shmblockname", O_RDWR|O_CREAT, 00777);
  if (-1 == shmfd) {//failed
    //err hanled
  }
  if (-1 == ftruncate(backend_store_handle, sizeof(RTSettings))) {
    printf("\n ftruncate failed\n");
    return;
  }
  mmap(NULL,
       sizeof(RTSettings),
       PROT_READ|PROT_WRITE,
       MAP_SHARED,
       backend_store_handle,
       SEEK_SET);
```

system V:
---

