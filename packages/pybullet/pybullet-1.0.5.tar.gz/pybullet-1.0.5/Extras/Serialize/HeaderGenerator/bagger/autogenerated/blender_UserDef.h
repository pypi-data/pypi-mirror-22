/* Copyright (C) 2006 Charlie C
*
* This software is provided 'as-is', without any express or implied
* warranty.  In no event will the authors be held liable for any damages
* arising from the use of this software.
*
* Permission is granted to anyone to use this software for any purpose,
* including commercial applications, and to alter it and redistribute it
* freely, subject to the following restrictions:
*
* 1. The origin of this software must not be misrepresented; you must not
*    claim that you wrote the original software. If you use this software
*    in a product, an acknowledgment in the product documentation would be
*    appreciated but is not required.
* 2. Altered source versions must be plainly marked as such, and must not be
*    misrepresented as being the original software.
* 3. This notice may not be removed or altered from any source distribution.
*/
// Auto generated from makesdna dna.c
#ifndef __BLENDER_USERDEF__H__
#define __BLENDER_USERDEF__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_ColorBand.h"
#include "blender_ListBase.h"
#include "blender_SolidLight.h"
#include "blender_WalkNavigation.h"

namespace Blender {


    // ---------------------------------------------- //
    class UserDef
    {
    public:
        int versionfile;
        int subversionfile;
        int flag;
        int dupflag;
        int savetime;
        char tempdir[768];
        char fontdir[768];
        char renderdir[1024];
        char render_cachedir[768];
        char textudir[768];
        char pythondir[768];
        char sounddir[768];
        char i18ndir[768];
        char image_editor[1024];
        char anim_player[1024];
        int anim_player_preset;
        short v2d_min_gridsize;
        short timecode_style;
        short versions;
        short dbl_click_time;
        short gameflags;
        short wheellinescroll;
        int uiflag;
        int uiflag2;
        int language;
        short userpref;
        short viewzoom;
        int mixbufsize;
        int audiodevice;
        int audiorate;
        int audioformat;
        int audiochannels;
        int scrollback;
        int dpi;
        char pad2[2];
        short transopts;
        short menuthreshold1;
        short menuthreshold2;
        ListBase themes;
        ListBase uifonts;
        ListBase uistyles;
        ListBase keymaps;
        ListBase user_keymaps;
        ListBase addons;
        ListBase autoexec_paths;
        char keyconfigstr[64];
        short undosteps;
        short undomemory;
        short gp_manhattendist;
        short gp_euclideandist;
        short gp_eraser;
        short gp_settings;
        short tb_leftmouse;
        short tb_rightmouse;
        SolidLight light[3];
        short tw_hotspot;
        short tw_flag;
        short tw_handlesize;
        short tw_size;
        short textimeout;
        short texcollectrate;
        short wmdrawmethod;
        short dragthreshold;
        int memcachelimit;
        int prefetchframes;
        short frameserverport;
        short pad_rot_angle;
        short obcenter_dia;
        short rvisize;
        short rvibright;
        short recent_files;
        short smooth_viewtx;
        short glreslimit;
        short curssize;
        short color_picker_type;
        char ipo_new;
        char keyhandles_new;
        char gpu_select_method;
        char view_frame_type;
        int view_frame_keyframes;
        float view_frame_seconds;
        short scrcastfps;
        short scrcastwait;
        short widget_unit;
        short anisotropic_filter;
        short use_16bit_textures;
        short use_gpu_mipmap;
        float ndof_sensitivity;
        float ndof_orbit_sensitivity;
        int ndof_flag;
        short ogl_multisamples;
        short image_draw_method;
        float glalphaclip;
        short autokey_mode;
        short autokey_flag;
        short text_render;
        short pad9;
        ColorBand coba_weight;
        vec3f sculpt_paint_overlay_col;
        vec4f gpencil_new_layer_col;
        short tweak_threshold;
        char navigation_mode;
        char pad;
        char author[80];
        char font_path_ui[1024];
        int compute_device_type;
        int compute_device_id;
        float fcu_inactive_alpha;
        float pixelsize;
        int virtual_pixel;
        short pie_interaction_type;
        short pie_initial_timeout;
        short pie_animation_timeout;
        short pie_menu_confirm;
        short pie_menu_radius;
        short pie_menu_threshold;
        WalkNavigation walk_navigation;
    };
}


#endif//__BLENDER_USERDEF__H__
