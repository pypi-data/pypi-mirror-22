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
#ifndef __BLENDER_FREESTYLELINESTYLE__H__
#define __BLENDER_FREESTYLELINESTYLE__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_ID.h"
#include "blender_ListBase.h"

namespace Blender {


    // ---------------------------------------------- //
    class FreestyleLineStyle
    {
    public:
        ID id;
        AnimData *adt;
        float r;
        float g;
        float b;
        float alpha;
        float thickness;
        int thickness_position;
        float thickness_ratio;
        int flag;
        int caps;
        int chaining;
        int rounds;
        float split_length;
        float min_angle;
        float max_angle;
        float min_length;
        float max_length;
        int chain_count;
        short split_dash1;
        short split_gap1;
        short split_dash2;
        short split_gap2;
        short split_dash3;
        short split_gap3;
        int sort_key;
        int integration_type;
        float texstep;
        short texact;
        short pr_texture;
        short use_nodes;
        short pad[3];
        short dash1;
        short gap1;
        short dash2;
        short gap2;
        short dash3;
        short gap3;
        int panel;
        MTex *mtex[18];
        bNodeTree *nodetree;
        ListBase color_modifiers;
        ListBase alpha_modifiers;
        ListBase thickness_modifiers;
        ListBase geometry_modifiers;
    };
}


#endif//__BLENDER_FREESTYLELINESTYLE__H__
