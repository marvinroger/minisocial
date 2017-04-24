/* global $ */

var FEED_REFRESH_INTERVAL_MS = 1000
var FEED_REFRESH_URL = window.FEED_REFRESH_URL // window.FEED_REFRESH_URL defined in the view
var LAST_STATE = window.LAST_STATE // window.LAST_STATE defined in the view

$(function () {
  // Handle message sending

  $('#form_post_message').on('submit', function onSubmit (e) {
    e.preventDefault()

    var submitButton = $(this).find('input[type=submit]')
    var messageInput = $(this).find('input[name=message]')
    var formUrl = $(this).attr('action')
    var formMethod = $(this).attr('method')
    var inputs = {}
    $(this).find('input').not('[type=submit]').each(function (index, input) {
      var name = $(input).attr('name')
      var value = $(input).val()
      inputs[name] = value
    })

    $(submitButton).attr('disabled', 'disabled')

    $.ajax({
      url: formUrl,
      type: formMethod,
      data: inputs
    }).done(function (data) {
      $(messageInput).val('')
    }).always(function () {
      $(submitButton).removeAttr('disabled')
    })
  })

  // Handle feed refreshing

  var lastState = LAST_STATE
  var feedRefreshTimeout
  var armFeedRefresh = function () {
    if (feedRefreshTimeout) clearTimeout(feedRefreshTimeout)

    feedRefreshTimeout = setTimeout(function handleFeedRefresh () {
      $.get(FEED_REFRESH_URL, { last_state: lastState }).done(function (data) {
        lastState = data.last_state
      }).always(function () {
        armFeedRefresh()
      })
    }, FEED_REFRESH_INTERVAL_MS)
  }

  armFeedRefresh()
})
