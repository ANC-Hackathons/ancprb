#include <pebble.h>

static Window *window;
static TextLayer *text_layer;

enum {
  BUTTON_PRESS_KEY = (uint32_t) 0,
  LEFT_PRESS = (uint8_t) 1,
  RIGHT_PRESS = (uint8_t) 2
};

static void select_click_handler(ClickRecognizerRef recognizer, void *context) {
  text_layer_set_text(text_layer, "Select");
}

static void send_simple_dict(uint32_t key, uint8_t val) {
  DictionaryIterator *iter;
  app_message_outbox_begin(&iter);

  if (iter == NULL)
    return;

  dict_write_uint8(iter, key, val);
  dict_write_end(iter);

  app_message_outbox_send();
}

static void up_click_handler(ClickRecognizerRef recognizer, void *context) {
  send_simple_dict(BUTTON_PRESS_KEY, LEFT_PRESS);
  text_layer_set_text(text_layer, "Up");
}

static void down_click_handler(ClickRecognizerRef recognizer, void *context) {
  send_simple_dict(BUTTON_PRESS_KEY, RIGHT_PRESS);
  text_layer_set_text(text_layer, "Down");
}

static void outbox_fail_callback(DictionaryIterator *iterator, AppMessageResult reason, void *context) {
  switch (reason) {
    case APP_MSG_SEND_TIMEOUT:
      APP_LOG(APP_LOG_LEVEL_ERROR, "APP_MSG_SEND_TIMEOUT");
      break;
    default:
      APP_LOG(APP_LOG_LEVEL_ERROR, "I have no idea");
  }
}

static void click_config_provider(void *context) {
  window_single_click_subscribe(BUTTON_ID_SELECT, select_click_handler);
  window_single_click_subscribe(BUTTON_ID_UP, up_click_handler);
  window_single_click_subscribe(BUTTON_ID_DOWN, down_click_handler);
}

static void window_load(Window *window) {
  Layer *window_layer = window_get_root_layer(window);
  GRect bounds = layer_get_bounds(window_layer);

  text_layer = text_layer_create((GRect) { .origin = { 0, 72 }, .size = { bounds.size.w, 20 } });
  text_layer_set_text(text_layer, "Press a button");
  text_layer_set_text_alignment(text_layer, GTextAlignmentCenter);
  layer_add_child(window_layer, text_layer_get_layer(text_layer));
}

static void window_unload(Window *window) {
  text_layer_destroy(text_layer);
}

static void init(void) {
  // Open AppMessage to transfers
  app_message_open(app_message_inbox_size_maximum(), app_message_outbox_size_maximum());
  app_message_register_outbox_failed(outbox_fail_callback);

  window = window_create();
  window_set_click_config_provider(window, click_config_provider);
  window_set_window_handlers(window, (WindowHandlers) {
    .load = window_load,
    .unload = window_unload,
  });
  const bool animated = true;
  window_stack_push(window, animated);
}

static void deinit(void) {
  window_destroy(window);
}

int main(void) {
  init();

  APP_LOG(APP_LOG_LEVEL_DEBUG, "Done initializing, pushed window: %p", window);

  app_event_loop();
  deinit();
}
