import $ from 'jquery'
import 'reconnectingwebsocket'

$(document).ready(function() {

  $('.logo__link').on('click', function(e) {
    e.preventDefault();
    $('html, body').animate({scrollTop: '0'}, 300, 'swing');
  });

  $('.card').on('click', function(e) {
    $(this).toggleClass('is-flipped');
  });

  $('.card__link a').on('click', function(e) {
    e.stopPropagation();
  });

  if (window.wsSessionKey) {

    var proto = window.location.protocol == 'https:' ? 'wss' : 'ws';
    var host = window.location.host;
    var socket = new ReconnectingWebSocket(
      proto + '://' + host + '/presentations?session_key=' + wsSessionKey);

    socket.onmessage = function(e) {
      console.log(e.data);
    }

    $('.js-select').on('click', function(e) {
      e.stopPropagation();

      var presId = $(this).data('presentation-id');
      var card = $(this).closest('.card');
      var $this = $(this);

      if ($this.attr('data-selected') === "true") {
        $this.removeClass('is-selected');
        $this.html('Add to Calendar');
        $this.attr('data-selected', 'false');
        card.removeClass('is-selected');
        socket.send("disinterested:" + presId);
      } else {
        $this.addClass('is-selected');
        $this.html('Remove from Calendar');
        $this.attr('data-selected', 'true');
        card.addClass('is-selected');
        socket.send("interested:" + presId);
      }
    });

  }

});
