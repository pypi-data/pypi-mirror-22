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
#ifndef __BLENDER_THEMEUI__H__
#define __BLENDER_THEMEUI__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_uiPanelColors.h"
#include "blender_uiWidgetColors.h"
#include "blender_uiWidgetStateColors.h"

namespace Blender {


    // ---------------------------------------------- //
    class ThemeUI
    {
    public:
        uiWidgetColors wcol_regular;
        uiWidgetColors wcol_tool;
        uiWidgetColors wcol_text;
        uiWidgetColors wcol_radio;
        uiWidgetColors wcol_option;
        uiWidgetColors wcol_toggle;
        uiWidgetColors wcol_num;
        uiWidgetColors wcol_numslider;
        uiWidgetColors wcol_menu;
        uiWidgetColors wcol_pulldown;
        uiWidgetColors wcol_menu_back;
        uiWidgetColors wcol_menu_item;
        uiWidgetColors wcol_tooltip;
        uiWidgetColors wcol_box;
        uiWidgetColors wcol_scroll;
        uiWidgetColors wcol_progress;
        uiWidgetColors wcol_list_item;
        uiWidgetColors wcol_pie_menu;
        uiWidgetStateColors wcol_state;
        uiPanelColors panel;
        char widget_emboss[4];
        float menu_shadow_fac;
        short menu_shadow_width;
        short pad[3];
        char iconfile[256];
        float icon_alpha;
        char xaxis[4];
        char yaxis[4];
        char zaxis[4];
    };
}


#endif//__BLENDER_THEMEUI__H__
