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
#ifndef __BLENDER_SPACECLIP__H__
#define __BLENDER_SPACECLIP__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_ListBase.h"
#include "blender_MaskSpaceInfo.h"
#include "blender_MovieClipScopes.h"
#include "blender_MovieClipUser.h"

namespace Blender {


    // ---------------------------------------------- //
    class SpaceClip
    {
    public:
        SpaceLink *next;
        SpaceLink *prev;
        ListBase regionbase;
        int spacetype;
        float xof;
        float yof;
        float xlockof;
        float ylockof;
        float zoom;
        MovieClipUser user;
        MovieClip *clip;
        MovieClipScopes scopes;
        int flag;
        short mode;
        short view;
        int path_length;
        float loc[2];
        float scale;
        float angle;
        int pad;
        float stabmat[4][4];
        float unistabmat[4][4];
        int postproc_flag;
        short gpencil_src;
        short pad2;
        int around;
        int pad4;
        float cursor[2];
        MaskSpaceInfo mask_info;
    };
}


#endif//__BLENDER_SPACECLIP__H__
