# Electron: jQuery is not defined


A better an more generic solution IMO:
---

```javascript
<!-- Insert this line above script imports -->
<script>
  if (typeof module === 'object') {
    window.module = module;
    module = undefined;
  }
</script> 
<!-- normal script imports etc --> 
<script src="scripts/jquery.min.js"></script> 
<script src="scripts/vendor.js"></script> 

<!-- Insert this line after script imports --> 
<script>
  if (window.module) 
    module = window.module;
</script>
```

**Benefits**

* Works for both browser and electron with the same code
* Fixes issues for ALL 3rd-party libraries (not just jQuery) without having to specify each one
* Script Build / Pack Friendly (i.e. Grunt / Gulp all scripts into vendor.js)
* Does NOT require `node-integration` to be false

