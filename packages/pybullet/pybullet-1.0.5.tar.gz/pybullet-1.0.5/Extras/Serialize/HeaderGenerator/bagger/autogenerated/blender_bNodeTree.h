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
#ifndef __BLENDER_BNODETREE__H__
#define __BLENDER_BNODETREE__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_ID.h"
#include "blender_ListBase.h"
#include "blender_bNodeInstanceKey.h"
#include "blender_rctf.h"

namespace Blender {


    // ---------------------------------------------- //
    class bNodeTree
    {
    public:
        ID id;
        AnimData *adt;
        bInvalidHandle *typeinfo;
        char idname[64];
        bInvalidHandle *interface_type;
        bGPdata *gpd;
        float view_center[2];
        ListBase nodes;
        ListBase links;
        int type;
        int init;
        int cur_index;
        int flag;
        int update;
        short is_updating;
        short done;
        int pad2;
        int nodetype;
        short edit_quality;
        short render_quality;
        int chunksize;
        rctf viewer_border;
        ListBase inputs;
        ListBase outputs;
        bInvalidHandle *previews;
        bNodeInstanceKey active_viewer_key;
        int pad;
        bInvalidHandle *execdata;
        void (*progress)();
        void (*stats_draw)();
        int (*test_break)();
        void (*update_draw)();
        void *tbh;
        void *prh;
        void *sdh;
        void *udh;
    };
}


#endif//__BLENDER_BNODETREE__H__
