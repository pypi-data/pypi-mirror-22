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
#ifndef __BLENDER_WMWINDOW__H__
#define __BLENDER_WMWINDOW__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_ListBase.h"

namespace Blender {


    // ---------------------------------------------- //
    class wmWindow
    {
    public:
        wmWindow *next;
        wmWindow *prev;
        void *ghostwin;
        bScreen *screen;
        bScreen *newscreen;
        char screenname[64];
        short posx;
        short posy;
        short sizex;
        short sizey;
        short windowstate;
        short monitor;
        short active;
        short cursor;
        short lastcursor;
        short modalcursor;
        short grabcursor;
        short addmousemove;
        int winid;
        short lock_pie_event;
        short last_pie_event;
        bInvalidHandle *eventstate;
        bInvalidHandle *curswin;
        bInvalidHandle *tweak;
        bInvalidHandle *ime_data;
        int drawmethod;
        int drawfail;
        ListBase drawdata;
        ListBase queue;
        ListBase handlers;
        ListBase modalhandlers;
        ListBase subwindows;
        ListBase gesture;
        Stereo3dFormat *stereo3d_format;
    };
}


#endif//__BLENDER_WMWINDOW__H__
