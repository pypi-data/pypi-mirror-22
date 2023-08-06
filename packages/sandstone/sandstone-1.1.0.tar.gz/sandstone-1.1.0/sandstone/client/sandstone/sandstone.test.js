'use strict';

(function() {
  getDependencies();

  function getDependencies() {
    var depList = ["ui.router", "sandstone.acemodes", "ui.bootstrap", "sandstone.websocketservice", "sandstone.broadcastservice", "sandstone.filesystemservice", "sandstone.filetreedirective", "sandstone.editor", "sandstone.filebrowser", "sandstone.terminal", "sandstone.slurm", "sandstone.kcenjro"];
    var sandstone = getSandstoneModule(depList);

    angular.element(document).ready(function() {
      angular.bootstrap(document, ['sandstone']);
    });
  }
}());
