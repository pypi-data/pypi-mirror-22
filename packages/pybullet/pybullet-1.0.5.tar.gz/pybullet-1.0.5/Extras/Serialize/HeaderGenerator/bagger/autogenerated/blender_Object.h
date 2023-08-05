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
#ifndef __BLENDER_OBJECT__H__
#define __BLENDER_OBJECT__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_ID.h"
#include "blender_ListBase.h"
#include "blender_bAnimVizSettings.h"

namespace Blender {


    // ---------------------------------------------- //
    class Object
    {
    public:
        ID id;
        AnimData *adt;
        bInvalidHandle *sculpt;
        short type;
        short partype;
        int par1;
        int par2;
        int par3;
        char parsubstr[64];
        Object *parent;
        Object *track;
        Object *proxy;
        Object *proxy_group;
        Object *proxy_from;
        Ipo *ipo;
        BoundBox *bb;
        bAction *action;
        bAction *poselib;
        bPose *pose;
        void *data;
        bGPdata *gpd;
        bAnimVizSettings avs;
        bMotionPath *mpath;
        ListBase constraintChannels;
        ListBase effect;
        ListBase defbase;
        ListBase modifiers;
        int mode;
        int restore_mode;
        Material **mat;
        char *matbits;
        int totcol;
        int actcol;
        vec3f loc;
        vec3f dloc;
        vec3f orig;
        vec3f size;
        vec3f dsize;
        vec3f dscale;
        vec3f rot;
        vec3f drot;
        vec4f quat;
        vec4f dquat;
        vec3f rotAxis;
        vec3f drotAxis;
        float rotAngle;
        float drotAngle;
        float obmat[4][4];
        float parentinv[4][4];
        float constinv[4][4];
        float imat[4][4];
        float imat_ren[4][4];
        int lay;
        short flag;
        short colbits;
        short transflag;
        short protectflag;
        short trackflag;
        short upflag;
        short nlaflag;
        short ipoflag;
        short scaflag;
        char scavisflag;
        char depsflag;
        int dupon;
        int dupoff;
        int dupsta;
        int dupend;
        int lastNeedMapping;
        float mass;
        float damping;
        float inertia;
        float formfactor;
        float rdamping;
        float margin;
        float max_vel;
        float min_vel;
        float obstacleRad;
        float step_height;
        float jump_speed;
        float fall_speed;
        short col_group;
        short col_mask;
        short rotmode;
        char boundtype;
        char collision_boundtype;
        short dtx;
        char dt;
        char empty_drawtype;
        float empty_drawsize;
        float dupfacesca;
        ListBase prop;
        ListBase sensors;
        ListBase controllers;
        ListBase actuators;
        float sf;
        short index;
        short actdef;
        vec4f col;
        int gameflag;
        int gameflag2;
        BulletSoftBody *bsoft;
        char restrictflag;
        char recalc;
        short softflag;
        vec3f anisotropicFriction;
        ListBase constraints;
        ListBase nlastrips;
        ListBase hooks;
        ListBase particlesystem;
        PartDeflect *pd;
        SoftBody *soft;
        Group *dup_group;
        char body_type;
        char shapeflag;
        short shapenr;
        float smoothresh;
        FluidsimSettings *fluidsimSettings;
        bInvalidHandle *curve_cache;
        bInvalidHandle *derivedDeform;
        bInvalidHandle *derivedFinal;
        bInvalidHandle lastDataMask;
        bInvalidHandle customdata_mask;
        int state;
        int init_state;
        ListBase gpulamp;
        ListBase pc_ids;
        ListBase *duplilist;
        RigidBodyOb *rigidbody_object;
        RigidBodyCon *rigidbody_constraint;
        float ima_ofs[2];
        ImageUser *iuser;
        ListBase lodlevels;
        LodLevel *currentlod;
    };
}


#endif//__BLENDER_OBJECT__H__
