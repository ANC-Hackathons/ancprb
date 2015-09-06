#include <pebble.h>
#include "main_window.h"

// BEGIN AUTO-GENERATED UI CODE; DO NOT MODIFY
static Window *s_window;
static GFont s_res_gothic_24;
static TextLayer *s_textlayer_1;

static ActionBarLayer *s_actionbarlayer_1;
static GBitmap *s_rotate_left_bitmap;
static GBitmap *s_rotate_right_bitmap;
static GBitmap *s_start_bitmap;

static Layer *s_canvas_layer_1;
static GBitmap *s_toaster_bitmap;

static void layer_update_proc(Layer *layer, GContext *ctx) {
  graphics_context_set_compositing_mode(ctx, GCompOpSet);
  graphics_draw_bitmap_in_rect(ctx, s_toaster_bitmap, gbitmap_get_bounds(s_toaster_bitmap));
}

static void initialise_ui(void) {
  s_window = window_create();
  Layer *window_layer = window_get_root_layer(s_window);
  #ifndef PBL_SDK_3
    window_set_fullscreen(s_window, 0);
  #endif

  s_res_gothic_24 = fonts_get_system_font(FONT_KEY_GOTHIC_24);
  // s_textlayer_1
  s_textlayer_1 = text_layer_create(GRect(0, 0, 110, 80));
  text_layer_set_text(s_textlayer_1, "Use the buttons to steer your toaster");
  text_layer_set_text_alignment(s_textlayer_1, GTextAlignmentCenter);
  text_layer_set_font(s_textlayer_1, s_res_gothic_24);
  layer_add_child(window_get_root_layer(s_window), (Layer *)s_textlayer_1);

  // s_actionbarlayer_1
  s_rotate_left_bitmap = gbitmap_create_with_resource(RESOURCE_ID_LEFT_ICON);
  s_rotate_right_bitmap = gbitmap_create_with_resource(RESOURCE_ID_RIGHT_ICON);
  s_start_bitmap = gbitmap_create_with_resource(RESOURCE_ID_START_ICON);
  s_actionbarlayer_1 = action_bar_layer_create();
  action_bar_layer_add_to_window(s_actionbarlayer_1, s_window);
  action_bar_layer_set_background_color(s_actionbarlayer_1, GColorRed);
  action_bar_layer_set_icon_animated(s_actionbarlayer_1, BUTTON_ID_UP, s_rotate_left_bitmap, true);
  action_bar_layer_set_icon_animated(s_actionbarlayer_1, BUTTON_ID_DOWN, s_rotate_right_bitmap, true);
  action_bar_layer_set_icon_animated(s_actionbarlayer_1, BUTTON_ID_SELECT, s_start_bitmap, true);
  layer_add_child(window_get_root_layer(s_window), (Layer *)s_actionbarlayer_1);

  // Create canvas Layer
  s_toaster_bitmap = gbitmap_create_with_resource(RESOURCE_ID_TOASTER);
  s_canvas_layer_1 = layer_create(GRect(25, 90, 144, 168));
  layer_set_update_proc(s_canvas_layer_1, layer_update_proc);
  layer_add_child(window_layer, s_canvas_layer_1);
}

static void destroy_ui(void) {
  window_destroy(s_window);
  text_layer_destroy(s_textlayer_1);
  action_bar_layer_destroy(s_actionbarlayer_1);
  layer_destroy(s_canvas_layer_1);
  gbitmap_destroy(s_rotate_left_bitmap);
  gbitmap_destroy(s_rotate_right_bitmap);
  gbitmap_destroy(s_start_bitmap);
  gbitmap_destroy(s_toaster_bitmap);
}
// END AUTO-GENERATED UI CODE

static void handle_window_unload(Window* window) {
  destroy_ui();
}

Window* show_main_window(void) {
  initialise_ui();
  window_set_window_handlers(s_window, (WindowHandlers) {
    .unload = handle_window_unload,
  });
  window_stack_push(s_window, true);
  APP_LOG(APP_LOG_LEVEL_DEBUG, "Done initializing, pushed window: %p", s_window);

  return s_window;
}

void hide_main_window(void) {
  window_stack_remove(s_window, true);
}
