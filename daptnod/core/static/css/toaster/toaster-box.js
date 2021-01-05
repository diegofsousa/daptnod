(function() {
  this.ToasterBox = function() {
      
      // globel variable
      this.toasterContainer = null;
      this.toasterCloseBtn = null;
      const _ = this;

      let defaults = {
          msg: '',
          duration: 3000,
          html: false,
          className: null,
          closeButton: true,
          maxWidth: 450,
          autoOpen: true,
          position: 'bottom-center', //'top-left', 'top-center', 'top-right', 'bottom-left', 'bottom-center', 'bottom-right', 
          backgroundColor: null,
          closeIcon: null
      }

      if(arguments[0] && typeof arguments[0] === "object") {
          this.options = extendDefaults(defaults, arguments[0]);
      }
      if(this.options.autoOpen) {
          _.openToaster();
      }
      setTimeout(function () { _.closeToaster() }, Number(this.options.duration));
  }

  ToasterBox.prototype.openToaster = function() {
      // build out toaster
      buildToaster.call(this)
      // Initialize Event Listeners
      initializeEvents.call(this);
      /*
      * After adding elements to the DOM, use getComputedStyle
      * to force the browser to recalc and recognize the elements
      * that we just added. This is so that CSS animation has a start point
      */
      window.getComputedStyle(this.toasterContainer).height;
  }

  ToasterBox.prototype.closeToaster = function() {
      const _ = this;
      if(_.toasterContainer.classList.contains('top-left') || 
      _.toasterContainer.classList.contains('top-center') || 
      _.toasterContainer.classList.contains('top-right')) {
          _.toasterContainer.style.webkitAnimation = "fadeoutTop .5s";
          _.toasterContainer.style.animation = "fadeoutTop .5s";
      }
      if(_.toasterContainer.classList.contains('bottom-left') || 
      _.toasterContainer.classList.contains('bottom-center') || 
      _.toasterContainer.classList.contains('bottom-right')) {
          _.toasterContainer.style.webkitAnimation = "fadeoutBottom .5s";
          _.toasterContainer.style.animation = "fadeoutBottom .5s";
      }
      // Code for Safari 3.1 to 6.0
      _.toasterContainer.addEventListener("webkitAnimationend", function() {
          _.toasterContainer.remove();
      });

      // Standard syntax
      _.toasterContainer.addEventListener("animationend", function() {
          _.toasterContainer.remove();
      });
  }
  
  // build toaster
  function buildToaster() {
      var docFrag, toasterMsg;
      
      this.toasterContainer = document.createElement('div');
      this.toasterContainer.classList.add('toaster-container');
      this.toasterContainer.classList.add(this.options.position);
      this.toasterContainer.style.maxWidth = this.options.maxWidth + 'px';
      if(this.options.backgroundColor !== null) {
          this.toasterContainer.style.backgroundColor = this.options.backgroundColor;
      }
      if(this.options.className !== null) {
          this.toasterContainer.classList.add(this.options.className);
      }
      // toaster message
      toasterMsg = document.createElement('span');
      toasterMsg.classList.add(`toaster-msg`);
      if(!this.options.html) {
          toasterMsg.innerText = this.options.msg;
      } else {
          toasterMsg.innerHTML = this.options.msg;
      }
      // append toaster message to container
      this.toasterContainer.append(toasterMsg);
      // close button
      if(this.options.closeButton) {
          this.toasterCloseBtn = document.createElement('button');
          this.toasterCloseBtn.setAttribute('type','button');
          this.toasterCloseBtn.classList.add(`toaster-close`);
          if(this.options.closeIcon) {
              this.toasterCloseBtn.innerHTML = this.options.closeIcon;
          } else {
              this.toasterCloseBtn.innerHTML = "<img src='/static/css/toaster/close.svg' alt='close icon' width='20' class='inverted'/>";
          }
          this.toasterContainer.append(this.toasterCloseBtn);
      }
      // create document fragment and append toaster to it
      docFrag = document.createDocumentFragment();
      docFrag.append(this.toasterContainer)
      // append Doc Fragment to body
      document.body.append(docFrag);
  }

  function initializeEvents() {
      if(this.toasterCloseBtn) {
          this.toasterCloseBtn.addEventListener('click', this.closeToaster.bind(this));
      }
  }
  // overwrite default property
  function extendDefaults(source, properties) {
      let property;
      for(property in properties) {
          if(properties.hasOwnProperty(property)) {
              source[property] = properties[property];
          }
      }
      return source;
  }
})();