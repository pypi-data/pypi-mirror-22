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
#ifndef __BLENDER_MESH__H__
#define __BLENDER_MESH__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_CustomData.h"
#include "blender_ID.h"

namespace Blender {


    // ---------------------------------------------- //
    class Mesh
    {
    public:
        ID id;
        AnimData *adt;
        BoundBox *bb;
        Ipo *ipo;
        Key *key;
        Material **mat;
        MSelect *mselect;
        MPoly *mpoly;
        MTexPoly *mtpoly;
        MLoop *mloop;
        MLoopUV *mloopuv;
        MLoopCol *mloopcol;
        MFace *mface;
        MTFace *mtface;
        TFace *tface;
        MVert *mvert;
        MEdge *medge;
        MDeformVert *dvert;
        MCol *mcol;
        Mesh *texcomesh;
        bInvalidHandle *edit_btmesh;
        CustomData vdata;
        CustomData edata;
        CustomData fdata;
        CustomData pdata;
        CustomData ldata;
        int totvert;
        int totedge;
        int totface;
        int totselect;
        int totpoly;
        int totloop;
        int act_face;
        vec3f loc;
        vec3f size;
        vec3f rot;
        int drawflag;
        short texflag;
        short flag;
        float smoothresh;
        int pad2;
        char cd_flag;
        char pad;
        char subdiv;
        char subdivr;
        char subsurftype;
        char editflag;
        short totcol;
        Multires *mr;
    };
}


#endif//__BLENDER_MESH__H__
