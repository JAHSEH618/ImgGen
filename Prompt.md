### 写真——晚霞
```plain
{
    "prompt": "(((natural white face:1.8))), ((clear face)), (masterpiece:1.0), (highest quality:1.12), (realistic), a girl with long hair, (look at viewer), with a teal background and an indigo sky, (sunset glow), ((light is weak)), gown, silk gown, ((stand on a flat field path)), ((the path stretched into the distance)), constant, vaporwave colors, a character portrait, detailed, 8k, (professional lighting:1.0), sunset, one person, photographed on a Fuji XT3, 50mm lens, F/2.8, HDR, 8k resolution, (cinematic film still style), <lora:MJ52:0.7>, <lora:Sweet girl clothes4:0.7>",
    "negative_prompt": "worst quality, low quality, illustration, 3d, 2d, painting, cartoons, sketch), tooth, open mouth, ((shade on skin)), shade on face, ((full body)), multi arms, ((bad hands)), bad arms, (((long arms))), long neck, long back, bad shoulders, warm colors, spot on skin, river",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "d6a48d3e20",
    "sampler_name": "DPM++ SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps":8,
    "cfg_scale": 1.5,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 2,
    "restore_faces": false,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.35,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 5,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 0.9,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}
```



![](https://cdn.nlark.com/yuque/0/2024/png/46822309/1724838533570-04cf80fe-c819-43f2-83cc-122671c1fed8.png)

### 写真——宇航员
```plain
{
    "prompt": "(Just one person), ((real photo)), astronaut, wear white space suit, clear clothing detail, a person (standing on the moon), detailed and lifelike, science fiction, (clear clothing texture), realistic style, ((Space suit)), the moon has craters on its surface, the background features the (black universe, moon building, distant earth), (raw photo:1.2), ((photorealistic:1.4)), best quality ,masterpiece, photographed on a Fuji XT3, 50mm lens, F/2.8, HDR, 8k resolution, cinematic film still style, <lora:Astro_Life:0.6>, <lora:MJ52:1>",
    "negative_prompt": "Two people, (blurry clothes), blurry background, ((shadow on skin)), overexposed highlights, (oversaturated colors), (unrealistic skin tones), ((high contrast)), Cartoon, abstract, painting, blurry, low quality, sketch, surreal, unrealistic, fantasy, monochrome, warm climate, indoors, crowded, messy, chaotic, low resolution, incomplete, distorted",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "d6a48d3e20",
    "sampler_name": "DPM++ SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps":7,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 2,
    "restore_faces": false,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.35,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 2,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 0.9,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}
```



![](https://cdn.nlark.com/yuque/0/2024/png/46822309/1724838438536-3eb6186f-201b-46c2-accb-750eef2c5be7.png)

### 写真——花田
```plain
{
    "prompt": "((clear face)), 1girl, flower field, white bright dress, summer, (clear clothing texture), silky hair, HDR, front face, upper body, textured, various postures, <lora:TWbabeXL01:0.4>, best quality ,masterpiece, photographed on a Fuji XT3, 50mm lens, F/2.8, HDR, 8k resolution, cinematic film still style, <lora:MJ52:1>",
    "negative_prompt": "worst quality, low quality, illustration, 3d, 2d, painting, cartoons, sketch), tooth, open mouth, ((shade on skin)), shade on face, ((full body)), multi arms, ((bad hands)), bad arms, (((long arms))), long neck, long back, bad shoulders, warm colors, spot on skin, hair in one's face",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "d6a48d3e20",
    "sampler_name": "DPM++ SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps":8,
    "cfg_scale": 1.5,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 2,
    "restore_faces": false,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.35,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 5,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 0.9,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}
```



![](https://cdn.nlark.com/yuque/0/2024/png/46822309/1724838692620-375c4787-27c7-43c9-a52b-867d1f06a7f5.png)

### 写真——海边
```plain
{
    "prompt": "best quality, masterpiece, realistic, photography,  ((light on skin)), ((((white skin)))), ((clean face)), ((((clean skin)))), ((straight smooth long hair)), natural light, ((natural skin colour)), blue sky, blue calm sea, sunshine, bright, beach, standing, (((waves))), spaghetti strap dress, best quality ,masterpiece, photographed on a Fuji XT3, 50mm lens, F/2.8, HDR, 8k resolution, cinematic film still style, <lora:MJ52:0.7>",
    "negative_prompt": "worst quality, low quality, illustration, 3d, 2d, painting, cartoons, sketch), tooth, open mouth, ((shade on skin)), shade on face, ((full body)), multi arms, ((bad hands)), bad arms, (((long arms))), long neck, long back, bad shoulders, warm colors, spot on skin, ((hair in her face)), ((((dark spots on the skin)))),  ((((dark spots on the face)))), ((locks of hair))",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "d6a48d3e20",
    "sampler_name": "DPM++ SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps":8,
    "cfg_scale": 1.5,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 2,
    "restore_faces": false,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.35,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 5,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 0.8,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}
```



![](https://cdn.nlark.com/yuque/0/2024/png/46822309/1724838755696-60d1b0c9-7042-4553-9734-45c5fe007fd9.png)

### 超级英雄——超人
```json
{
    "prompt": "(((((semi realism))))), ((futuristic)), Semi-realistic digital painting of Superman, ((black Adam suit)), battling Kryptonians at night in the vastness of space, with (futuristic Kryptonian ships) in the background. The environment is filled with the (stars and distant galaxies), emphasizing a (futuristic, fancy atmosphere). Superman's cape flows dramatically as he engages in combat, showcasing (intense energy and movement). The image captures the (epic scale of the confrontation) without showing hands.((Six packs)), <lora:MJ52:0.3>, <lora:xl_more_art-full_v1:0.7>, <lora:SemiRealPonyXL:1>",
    "negative_prompt": "((white spots)), Low detail, static pose, empty background, blurry, low resolution, crowded scene, unrelated characters, bad hands",
    "model_name": "Nuclear General Purpose.safetensors",
    "model_hash": "6f4322fb22",
    "sampler_name": "DPM++ SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 10,
    "cfg_scale": 4,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 2,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": false,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.65,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 5,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": "https://modelsbucket2405.s3.us-west-2.amazonaws.com/elder.png"
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": "https://modelsbucket2405.s3.us-west-2.amazonaws.com/model1.png"
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}
```



![](https://cdn.nlark.com/yuque/0/2024/png/46822309/1724838796155-2eb1931a-218a-419a-b765-a6a4a40071c6.png)

### 超级英雄——美国队长
```json
{
    "prompt": "(((((semi realism)))))((futuristic))science fiction battle scene with Captain America (in a battle-worn suit with a star emblem on the chest) (holding his iconic shield with a star in the center), standing (amidst futuristic technology) (amidst explosions) and (amidst debris), resembling (the intense combat setting) from Avengers: Endgame. The overall atmosphere is (dark and dramatic) with a sense of urgency and heroism.<lora:MJ52:0.3> <lora:xl_more_art-full_v1:0.7> <lora:SemiRealPonyXL:1>",
    "negative_prompt": "((white spots))Low detail, static pose, empty background, blurry, low resolution, crowded scene, unrelated characters, bad hands",
    "model_name": "Nuclear General Purpose.safetensors",
    "model_hash": "6f4322fb22",
    "sampler_name": "DPM++ SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 10,
    "cfg_scale": 4,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 2,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": false,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.65,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 5,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 0.9,
            "input_image": {
                "image_url": "https://modelsbucket2405.s3.us-west-2.amazonaws.com/elder.png"
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 0.9,
            "input_image": {
                "image_url": "https://modelsbucket2405.s3.us-west-2.amazonaws.com/model1.png"
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}
```



![](https://cdn.nlark.com/yuque/0/2024/png/46822309/1724838808337-767d1c3a-d85b-4dbe-839f-815dabc2565e.png)

### 波普风格
```plain
{
    "prompt": "masterpiece,best quality, ( clear image,high resolution,sharp focus:1.2), newest, art by Andy Warhol and Roy Lichtenstein,<lora:popart:1>, popart, prtxztl,(1girl, solo:1.2),portrait, upper body,  beautiful  dress, jewelry, blue eyes, earrings, (blonde hair:1.2), red lipstick, makeup, looking at viewer ,(vibrant colors, flat color:1.2),screen printing, halftone printing, contemporary art, modern art, graphic art, commercial art, bold colors, bold lines, comic style, comic art, advertising art, kitsch, retro style, (gradient background:1.2), illustration,  ligne claire,eyeshadow, Bright colors,",
    "negative_prompt": "3d, realistic,blur,blurry, anime,multiple girls,multiple heads, lowres,bad anatomy,,error,missing fingers,extra digit,fewer digits,cropped,worst quality,low quality,normal quality,jpeg artifacts,signature,watermark,username,blurry,artist name, cartoon, superhero,naked, (bad hands, bad anatomy, bad body, bad face, bad teeth, bad arms, bad legs, deformities:1.3) (ugly hands, ugly anatomy, ugly body, ugly face, ugly teeth, ugly arms, ugly legs, deformities:1.3) ugly fingers, bad fingers, (((ugly nipples, bad nipples, deformed nipples))), (((Bad teeth, ugly teeth))),(text,logo,name, watermark:1.1),Disorder,  (colored skin,colored face:1.2),  Picture frame, Incomplete,censored, wrinkles, deformed, mutated, nude, nudity, nsfw, naked,dark skin, yellow background,  duplicate, monochrome ,shaded face,pot,colored skin,blue face,blue skin,sideway",
    "model_name": "animagine-xl-3.1.safetensors",
    "model_hash": "e3c47aedb0",
    "sampler_name": "Euler_Smea_Dy",
    "batch_size": 1,
    "n_iter": 1,
    "steps":45,
    "cfg_scale": 6,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "Automatic",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.4,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 12,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight":1.4,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}
```



![](https://cdn.nlark.com/yuque/0/2024/jpeg/46822309/1724640115732-9282e542-192b-4766-8914-8d3099134df0.jpeg)

### 杂志封面风格
```plain
{
    "prompt": "masterpiece, best quality, realistic, <lora:VOGUE_Fashion_Magazine_Cover_Vintage_1960-1975_SDXL:0.7>,Vogue, (magazine cover, editorial,big title text, English text, Colored text:1.4), a young woman,looking at viewer, beautiful dress, long hair,(Fluffy hair:0.9), diamond necklace,sideways,  movie themed style, epic cinematic photorealism style, artistic creative style, dramatic cinematic light style, cinematic color style, (street background:1.3), shot on film, epic, Gorgeous,photography,<lora:polyhedron_all_sdxl-000004:0.3>,celluloid film skintone color style,Kodak",
    "negative_prompt": "anime, cartoon, graphic,  painting, crayon, graphite, abstract, glitch, deformed, mutated, ugly, disfigured, ugly, deformed, noisy, blurry, low contrast, noise, noisy, ugly breasts, tripod, camera, (censorship, censored, worst quality, low quality, normal quality, lowres, low details, bad photo, bad photography, bad art:1.4), (blur, blurry), morbid, ugly, mutated malformed, mutilated, poorly lit, bad shadow, draft, cropped, out of frame, cut off, censored, JPEG artifacts, out of focus, glitch, duplicate, (bad hands, bad anatomy, bad body, bad face, bad teeth, bad arms, bad legs, deformities:1.3) (ugly hands, ugly anatomy, ugly body, ugly face, ugly teeth, ugly arms, ugly legs, deformities:1.3) ugly fingers, bad fingers, (((ugly nipples, bad nipples, deformed nipples))), (((Bad teeth, ugly teeth)))",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "d6a48d3e20",
    "sampler_name": "DPM++ 3M SDE",
    "batch_size": 1,
    "n_iter": 1,
    "steps":10,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "Automatic",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.3,
        "hr_scale": 2,
        "hr_upscaler": "Latent",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight":1.3,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}
```



![](https://cdn.nlark.com/yuque/0/2024/jpeg/46822309/1724639926775-91ffb9b9-f6b8-46f1-9a76-d441e9e0cefd.jpeg)



### 写真——海底
```plain
{
    "prompt": "1girl, ((realistic)), ((natural skin colour)), under the sea, (((under sea))) ,(beautiful detailed water), ((clean face)), ((((clean skin)))), dynamic angle, (blue tone), minnow, starfish, detailed light, dress, (((Tyndall effect))),panorama, (((swim like a mermaid))), whole body, best quality ,masterpiece, photographed on a Fuji XT3, 50mm lens, F/2.8, HDR, 8k resolution, cinematic film still style, <lora:MJ52:0.7>",
    "negative_prompt": "worst quality, low quality, illustration, 3d, 2d, painting, cartoons, sketch), tooth, open mouth, ((shade on skin)), shade on face, ((full body)), multi arms, ((bad hands)), bad arms, (((long arms))), long neck, long back, bad shoulders, warm colors, spot on skin, ((hair in her face)), ((((dark spots on the skin)))),  ((((dark spots on the face)))), ((locks of hair))",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "d6a48d3e20",
    "sampler_name": "DPM++ SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps":8,
    "cfg_scale": 1.5,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 2,
    "vae": "Automatic",
    "restore_faces": false,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.35,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 4,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}
```

![](https://cdn.nlark.com/yuque/0/2024/png/46822309/1724226632071-2515c3c4-d72d-4dd9-aaa9-6402cb58f2a2.png?x-oss-process=image%2Fformat%2Cwebp%2Fresize%2Cw_1240%2Climit_0)

### 赛博朋克
```plain
{
    "prompt": "1girl, solo, upper body, (((one face))), ((look at the viewer)), ((clear face)), Lucy, cyberpunk, asymmetrical hair, blue and green and pink hair, multicolored hair, blue eyes, eyeliner, eyeshadow, makeup, bare shoulders, bodysuit, futuristic, hologram, holographic face, ui, interface, nodes, particles, depth of field, bokeh, masterpiece, <lora:LucyXL:0.7>, <lora:PerfectEyesXL:1>, <lora:holoportraitv1:0.7>",
    "negative_prompt": "((((two faces)))), ((big chest)), ((bad face)), long body, (long neck), bad arms, (bad shoulders),  lowres, ((worst quality)), low quality, normal quality, very displeasing, realistic",
    "model_name": "animagine-xl-3.1.safetensors",
    "model_hash": "e3c47aedb0",
    "sampler_name": "DPM++ SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps":35,
    "cfg_scale": 8,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 2,
    "vae": "Automatic",
    "restore_faces": false,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.35,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 18,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1.35,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 0.9,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}
```

![](https://cdn.nlark.com/yuque/0/2024/png/46822309/1724227024986-d154ccbb-c457-4648-a86b-e6878b67ba94.png?x-oss-process=image%2Fformat%2Cwebp%2Fresize%2Cw_1240%2Climit_0)

### 超级英雄——蜘蛛侠
```plain
{
    "prompt": "masterpiece, best quality,  (((((semi realism)))))((futuristic)),man,solo,Iron Spider suit,(without the mask:1.5),serious,  in a battle scene from 'Endgame.' The background features a (((futuristic)), sci-fi cityscape) with towering buildings and advanced cyberpunk technology, all rendered in (semi-realism). Spider-Man's suit is detailed with (metallic, red and gold accents), (glowing blue eyes), and ((mechanical spider legs extending from his back)). The atmosphere is (tense and dynamic), with (debris and energy beams flying around) and a (massive explosion in the background), creating dramatic, fiery effects that illuminate the scene and capture the intensity of the battle.<lora:MJ52:0.3> <lora:xl_more_art-full_v1:0.7> <lora:SemiRealPonyXL:1>,long short",
    "negative_prompt": "((white spots))Low detail, static pose, empty background, blurry, low resolution, crowded scene, unrelated characters, (bad hands, bad anatomy, bad body, bad face, bad teeth, bad arms, bad legs, deformities:1.3), mask on head, laughing, smile, grip, ugly eyes, (multiple boys, multiple heads:1.2),(mask on head, helmet, face mask,masked , mouth mask, surfaces:1.3)",
    "model_name": "Nuclear General Purpose.safetensors",
    "model_hash": "6f4322fb22",
    "sampler_name": "DPM++ 2M Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps":80,
    "cfg_scale": 3,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.35,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}
```



![](https://cdn.nlark.com/yuque/0/2024/jpeg/46822309/1724639353462-9d5cfc9e-63b9-4396-92db-30a34be09f0c.jpeg)

### 超级英雄——钢铁侠
```plain
{
    "prompt": "masterpiece, best quality,serious,   (((((semi realism))))) Iron Man in a (Mark 72 suit), standing in front of the surface of a (futuristic spacecraft) with (((the vast expanse of space))) in the background. Iron Man's suit is illuminated by a (bright chest light), emitting sparks and showing signs of (intense battle). In the background, ((several figures)) in (similar suits) are flying with (jetpacks),(looking at viewer:1.3),  leaving trails of (fire and smoke). Behind Iron Man, the (spacecraft is exploding), creating a (dramatic burst of light and debris). The sky is filled with (distant stars) and (galaxies), and the spacecraft surface is covered in (high-tech machinery and glowing panels). The scene has a (dramatic and epic atmosphere).<lora:MJ52:0.3> <lora:xl_more_art-full_v1:0.7> <lora:SemiRealPonyXL:1>",
    "negative_prompt": "Low detail, static pose, empty background, blurry, low resolution, crowded scene, unrelated characters, bad hands.smile,grip,laughing, (mask on head, helmet, face mask,masked , mouth mask, surfaces:1.3)",
    "model_name": "Nuclear General Purpose.safetensors",
    "model_hash": "6f4322fb22",
    "sampler_name": "DPM++ 2M Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps":80,
    "cfg_scale": 3,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.35,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}
```



![](https://cdn.nlark.com/yuque/0/2024/jpeg/46822309/1724639353462-9d5cfc9e-63b9-4396-92db-30a34be09f0c.jpeg)

### 写真——冰川
```plain
{
    "prompt": "masterpiece, best quality, photography,looking at viewer, solo focus, character in the middle,  (Just one person), ((natural white skin tone)), ((natural color saturation)), (balanced contrast), A person (standing in front of an Antarctic glacier), detailed and lifelike, realistic style. ((Summer clothes)), creating a striking contrast against the icy backdrop, with hair slightly tousled by the cold breeze. The background features the (vast expanse of the Antarctic glacier with extensive blue ice formations), capturing the awe-inspiring beauty and scale of the natural landscape. The lighting highlights the (crisp, cold atmosphere) with a clear blue sky and occasional clouds",
    "negative_prompt": "Two people, blurry background, ((shadow on skin)), overexposed highlights, (oversaturated colors), (unrealistic skin tones), ((high contrast)), Cartoon, abstract, painting, blurry, low quality, sketch, surreal, unrealistic, fantasy, monochrome, warm climate, indoors, crowded, messy, chaotic, low resolution, incomplete, distorted,(bad hands, bad anatomy, bad body, bad face, bad teeth, bad arms, bad legs, deformities:1.3) (ugly hands, ugly anatomy, ugly body, ugly face, ugly teeth, ugly arms, ugly legs, deformities:1.3)",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "d6a48d3e20",
    "sampler_name": "DPM++ SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps":10,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "Automatic",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.35,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 5,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}
```

![](https://cdn.nlark.com/yuque/0/2024/jpeg/46822309/1724639749113-227db7b1-4a26-4628-b33b-90c184e6b1bb.jpeg)

### 写真——天空
```plain
{
    "prompt": "masterpiece, best quality, photography,film shot,( full body,long short, upper body:1.2),   (Levitation Photography by Annu Palakunnathu Matthew and Kiino Villand:1.2),  1girl, solo,(looking at viewer:1.2),  shiny skin,white skin,  floating,sky background,sunlight,(doves:0.95),clouds,sunlight,  fantasy, floating,  (dancing pose,beautiful pose:1.2),artistry,elegant, beautiful Dior dress, award-winning photography, aesthetic and beauty, raw details, crisp details, f/5.6, game-changing, multiple exposure photography, (center composition, symmetry composition:0.1),  <lora:MJ52:0.5> <lora:- SDXL - vanta-black_contrast_V3.0:0.5>,<lora:HandFineTuning_XL:0.8>,tools,tool,hand",
    "negative_prompt": "naked,nsfw, flowers, oil, paint splash, oil effect, dots, paint, freckles, liquid effect,,  bad quality, lowres,  bad anatomy, signature, text, error, cropped, jpeg artifacts,(bad hands, bad anatomy, bad body, bad face, bad teeth, bad arms, bad legs,bad fingers,bad eyes, deformities:1.3), (ugly hands, ugly anatomy, ugly body, ugly face, ugly teeth, ugly arms, ugly legs,ugly fingers,ugly eyes, deformities:1.3),Incomplete, multiple girls,(bad edges,broken edges gray edges :1.2) , (censorship, censored, worst quality, low quality, normal quality, lowres, low details, bad photo, bad photography, bad art:1.4),wall, building",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "d6a48d3e20",
    "sampler_name": "DPM++ SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 8,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "Automatic",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.35,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}
```

![](https://cdn.nlark.com/yuque/0/2024/jpeg/46822309/1724640341212-7194a2bf-9a3b-456c-8913-7087d739b28b.jpeg)

### 写真——森林公主
```plain
{
    "prompt": "masterpiece, best quality, photography, fantasy art style, Fantasy portrait,full body,  ethereal and dreamlike,inspired by the work of Arthur Rackham,falling golden sparks add a magical touch to the scene, (mystical forest background:1.1) ,(flying colorful butterflies:1.3) BREAK  1girl, solo,(looking at viewer:1.2),smile,long blonde hair,Wearing a garland on the head, standing in the lush forest, princess BREAK <lora:dress:0.5>,<lora:绪儿XL 丝路流光裙 XUER Silk Road glowing dress:0.9>,XUER Silk Road glowing dress,(glowing Transparent dress:1.4),Detailed clothes description,jewelry,bracelet,glowin, elegent pose, <lora:Fairy_Style_SDXL:0.7>,ais-fairy BREAK (decorative light bulbs hang from the tree:1.5),plants,rainforest, jungle gown, tree, mist, ethereal atmosphere,  sunlight,royal and nature light,looking majestic in forest,depth of field, <lora:HandFineTuning_XL: 0.65>,hand,tools,tool, Heads-up shooting",
    "negative_prompt": "naked,nsfw, oil, paint splash, oil effect, dots, paint, freckles, liquid effect,,  bad quality, lowres,  bad anatomy, signature, text, error, cropped, jpeg artifacts,(bad hands, bad anatomy, bad body, bad face, bad teeth, bad arms, bad legs,bad fingers,bad eyes, deformities:1.3), (ugly hands, ugly anatomy, ugly body, ugly face, ugly teeth, ugly arms, ugly legs,ugly fingers,ugly eyes, deformities:1.3),Incomplete, multiple girls,(bad edges,broken edges gray edges :1.2) , (censorship, censored, worst quality, low quality, normal quality, lowres, low details, bad photo, bad photography, bad art:1.4),trunk,fat",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "d6a48d3e20",
    "sampler_name": "DPM++ SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 8,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "Automatic",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.5,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1.2,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}
```



![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1726819842919-efd9a657-32e6-4b9d-87fb-8aa689a2c3be.png)

### 写真——红毯
```plain
{
    "prompt": "masterpiece, best quality, photography,realistic, Celebrity scenes,Banquet Hall,Spacious hall,A grand,wide sweeping staircase with a golden railing leading up to a landing with a painted ceiling, The staircase is made of white marble and has a golden railing ,red carpet spotlight BREAK movie star, (solo:1.3),standing on the ground,looking at viewer,smile, earrings, necklace,   self - confident,elegant pose,  Gorgeous dresses, full body, <lora:7a8684c1-aa8f-4e58-ab05-2f1981c3998c.TA_trained:0.5>,corset gown  ,<lora:Detailed_female_hands-000001:0.5>, tools,hand,tool,  wide angle lens, soft lighting, warm colors, high contrast, shallow depth of field, smooth texture",
    "negative_prompt": "naked,nsfw, oil, paint splash, oil effect, dots, paint, freckles, liquid effect,,  bad quality, lowres,  bad anatomy, signature, text, error, cropped, jpeg artifacts,(bad hands, bad anatomy, bad body, bad teeth, bad arms, bad legs,bad fingers,bad eyes, deformities:1.3), (ugly hands, ugly anatomy, ugly body, ugly teeth, ugly arms, ugly legs,ugly fingers,ugly eyes, deformities:1.3),Incomplete, multiple girls,(bad edges,broken edges gray edges :1.2) , (censorship, censored, worst quality, low quality, normal quality, lowres, low details, bad photo, bad photography, bad art:1.4),multiple girls, bad fingernails,ugly fingernails,pillar,corridor,hallway",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "  d6a48d3e20",
    "sampler_name": "   DPM++ SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 6,
    "cfg_scale": 1,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "Automatic",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.35,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 4,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}
```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1724909426179-3ba4cc63-fbea-4252-b8aa-71edad7e6d3a.png)

### 写真——海边假日
```plain
{
    "prompt": "masterpiece, best quality, photography, realistic,  A young woman with long, flowing hair and piercing  eyes, looking at viewer,(wide-brimmed straw hat:0.8) and a white silk blouse, flowers on the hat,  shiny skin,makeup, lipstick, smile, detailed eyes, (falling petals on the screen:1.2) BREAK  blurred beach scene and Flowers and mountain, with the turquoise ocean and golden sand visible in the distance,soft natural light,, warm colors, focus on the woman's face, shallow depth of field,sunlight,datlight,sunny, high contrust,  85mm lens",
    "negative_prompt": "naked,nsfw, oil, paint splash, oil effect, dots, paint, freckles, liquid effect,,  bad quality, lowres,  bad anatomy, signature, text, error, cropped, jpeg artifacts,(bad hands, bad anatomy, bad body, bad teeth, bad arms, bad legs,bad fingers,bad eyes, deformities:1.3), (ugly hands, ugly anatomy, ugly body, ugly teeth, ugly arms, ugly legs,ugly fingers,ugly eyes, deformities:1.3),Incomplete, multiple girls,(bad edges,broken edges gray edges :1.2) , (censorship, censored, worst quality, low quality, normal quality, lowres, low details, bad photo, bad photography, bad art:1.4),multiple girls, bad fingernails,ugly fingernails,pillar,open mouth",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "d6a48d3e20",
    "sampler_name": "DPM++ SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 8,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "Automatic",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.35,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```



### 艺术照——戴珍珠耳环的少女
```plain
{
    "prompt": "a painting of a girl with a pearl earring <lora:JohannesVermeerXL_v1:1>,JohannesVermeerXL, Portrait painting, inspired by the work of Johannes Vermeer,A young woman with [A (deep blue:1.3) headscarf : a loose yellow knot at the back of her head:0.5], with the (yellow ends:1.1) (falling down her neck in a graceful cascade:1.1)BREAK (deep dark yellow cloth:1.3) BREAK small White collar, a large white pearl earring,looking at viewer,  oil painting, soft lighting,high contrust, focus on the woman's face, dark background",
    "negative_prompt": "Watermark, Text, censored, deformed, bad anatomy, disfigured, poorly drawn face,(Neck lines,wrinkles,rugose,furrow:1.2),(pearls necklace,necklace:1.3),(ugly neck,hair:1.3), mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet,  abnormal fingers,",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "d6a48d3e20",
    "sampler_name": "Euler a",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 10,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.35,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1725348810701-c7ab07ae-86cc-4bbc-ac10-5d40d3302548.png)

### 艺术照——星空
```plain
{
    "prompt": "Impressionist painting, vibrant and expressive, inspired by Vincent van Gogh,<lora:Van_gogh_by_DevDope-000014:0.5>,Van gogh style,galaxy sky in van gogh style, solo,elegent,smile, holding a small bouquet of sunflowers, looking at viewer, standing in the background of Van Gogh's starry sky,thick brushstrokes, swirling lines, focus on the figure, background blurred, 50mm lens,<lora:鲜创一派@Lady Hand_SDXL:0.5>,XCYP Lady Hand,Lady Hand",
    "negative_prompt": "(Watermark, Text,name,character name:1.2),  Multiple wings, censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet,  abnormal fingers,blank edge",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "d6a48d3e20",
    "sampler_name": "Euler a",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 10,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.35,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1725848637819-0ac12a87-36ba-484e-af3c-9fdfb68b1b04.png)

### 艺术照——蒙娜丽莎
```plain
{
    "prompt": "masterpiece,best quality,<lora:tbh191-sdxl:0.6>,illustration,style of Leonardo da Vinci,Mona Lisa,The background is a soft, hazy landscape, with distant mountains and a river winding through the valley,portrait,Turn sideways to the left,elegant, sitting,dark and flowing hair with a hint of reddish-brown tones,deep and velvet( black:1.1) gown with a subtle sheen, The sleeves are slightly puffed at the shoulders,(hands crossed over her lap:1.2),<lora:鲜创一派@Lady Hand_SDXL:0.6>,XCYP Lady Hand,Lady Hand",
    "negative_prompt": "(Watermark, Text,name,character name:1.2),  Multiple wings, censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet,  abnormal fingers,",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "d6a48d3e20",
    "sampler_name": "Euler a",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 10,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.2,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1726193466040-b95528c3-8551-420b-8829-1b2d1dd4a487.png)

### 艺术照——撑阳伞的少女
```plain
{
    "prompt": "masterpiece, best quality, Impressionist painting, airy and delicate, inspired by Claude Monet, <lora:Monet_XL:1>,cmnt,solo,full body, (looking at viewer:1.3),(detailed eyes,detailed face:1.3), A woman in a flowing white dress,white hat, one hand holding a green and white parasol ,The other hand hangs down at her side,[blue sky: flower field:0.7], <lora:鲜创一派@Lady Hand_SDXL:0.7>,XCYP Lady Hand,Lady Hand, blurred background,(oil painting, drawing, sketch:1.3),",
    "negative_prompt": "realistic,  (Watermark, Text,name,character name:1.3),gloves, ( Multiple wings:1.2), censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet,  abnormal fingers,",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "d6a48d3e20",
    "sampler_name": "Euler a",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 10,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.2,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1.4,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1726219477179-d8052314-7ff4-445a-be0f-0de3bd70321b.png)

### 艺术照——粉玫瑰
```plain
{
    "prompt": "<lora:Proskurin_oil_painting_style:0.7>,oil painting,Impressionist painting,young woman,detailed eyes,looking at viewer,gentle smile, soft brown eyes, sitting in the garden ,elegant pose,Elegant temperament,short hair,delicate white ribbon around her head, white dress with flowing skirt and fitted bodice, adorned with pink roses, holding a single pink rose in one hand, petals unfurling in the light, soft blur of (hazy sky:1.2) background,sunlight, peaceful tranquility,<lora:鲜创一派@Lady Hand_SDXL:0.6>,XCYP Lady Hand,Lady Hand",
    "negative_prompt": "(realistic, photography:1.2), Watermark, Text, censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands,bad arms,ugly arms, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet,  abnormal fingers,",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "d6a48d3e20",
    "sampler_name": "Euler a",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 10,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.2,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1.2,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1726736601699-992011ed-bb7a-4d80-ba2e-6d71601d8ad1.png)

### 写真——人间芭比
```plain
{
    "prompt": "best quality,portrait photography,masterpiece,1girl,solo,barbie, magical,cosmetics floating in the air,Holding a doll,looking at viewer,elegant pose,blue eyes,(pink satin bow in hair:1.3),(pink balloons in background:1.3) ,pink background,solid background,pink dress,jewelry,makeup,lipstick,dreamy and alluring,<lora:polyhedron_all_sdxl-000004:0.5>,<lora:Sweet girl clothes4:0.7>,perfect skin,detailed skin,shiny skin,no skin blemish,shimmering makeup,styled hair,flawless complexion,elegant attire, <lora:鲜创一派@Lady Hand_SDXL:0.6>,XCYP Lady Hand,Lady Hand,long shot,<lora:Long_hair_SDXL:0.7>,long hair,facing camera,wavy hair,massive hair,blonde hair",
    "negative_prompt": "Naked,nsfw，(Bare shoulders:1.4)，pot,blur,blurry, censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers,bad arms",
    "model_name": "Nuclear General Purpose.safetensors",
    "model_hash": "6f4322fb22",
    "sampler_name": "Euler a",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 40,
    "cfg_scale": 3,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae":sdxl_vae.safetensors,
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.3,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1727680747771-2e310966-b90e-4106-950d-7add1958db7b.png)

### 女童写真——爱莎公主
```plain
{
    "prompt": "masterpiece, best quality,fantasy,1girl, solo, Princess Elsa,collar,1girl,solo,<lora:xl0918ice-water:1.2>,water,ice and water,water ring,the ink ring surrounds the girl (lingering:1.2) and is a bit of a circular magic,ice,(ink splash:1.2),Splashing water,A braid, draped over the shoulder,wears a beautiful ice-blue gown adorned with sparkling crystals and a snowflake tiara,A crown set with diamonds  snow,(romanticism:1.1),film,highly detailed,Glass fragments,Shimmering Crysta,backlighting,((floating)),dynamic angle,beautiful detailed glow,(floating palaces:1.2),((detailed beautiful snow forest with trees)),((snowflakes)),floating,<lora:StS_age_slider_v1_initial_release:-2>",
    "negative_prompt": "Naked,nsfw，text,logo, censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers,bad arms",
    "model_name": "Nuclear General Purpose.safetensors",
    "model_hash": "6f4322fb22",
    "sampler_name": "Euler a",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 40,
    "cfg_scale": 3,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae":sdxl_vae.safetensors,
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.3,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1727148076239-dfda852a-64ee-4581-8efc-6a3c1c184ba8.png)

### 女童写真——人鱼公主
```plain
{
    "prompt": "masterpiece, best quality,HDR,8k resolution,realistic,blue tone, 1girl,solo,looking at viewer,full body,Disney Mermaids, Mermaid Ariel,underwater,beautiful detailed water,Sit on the reef,blue tail,long red hair,Fluffy hair,shimmering teal tail, surrounded by playful fishes,Sunlight streams down from above,( illuminating the scene with a magical glow:1.2),large Bubbles in the foreground,(Abyssal background:0.8), (coral:0.5), vibrant colors, blurred background,<lora:StS_age_slider_v1_initial_release:-1>, <lora:鲜创一派@Lady Hand_SDXL:0.6>,XCYP Lady Hand,Lady Hand,<lora:MJ52:0.7>,<lyco:SDXL_LoCon_mermaid_dataset_WCoff_bt04_ep016_09800_1024_dim128_a064_con064_a032_LR00010_snr05_noise00_del:0.7>",
    "negative_prompt": "Naked,nsfw,(red tail,multiple tails:1.4), (multiple girls:1.4),watermark,text,logo, censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers,bad arms ",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "d6a48d3e20",
    "sampler_name": "Euler a",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 6,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.3,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1727419024295-4cdf2235-7920-44e2-9706-977424e25c71.png)

### 男童写真——机甲
```plain
{
    "prompt": "masterpiece, best quality,8k,HDR, <lora:mecha-000009 (1):0.8>,mecha,1boy,solo, without mask,serious,(looking at viewer:1.2),  standing, all rendered in (semi-realism),The background features a ((futuristic)),city,skyscrapers background,sparks,Halo,flare,flow,explosion, background blur, <lora:StS_age_slider_v1_initial_release:-1>,",
    "negative_prompt": "Naked,nsfw，mouth open,watermark,text,logo, censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers,bad arms,(mask on head,helmet,horn, face mask,masked , mouth mask, surfaces:1.3),bad body proportions,pot,broken",
    "model_name": "Nuclear General Purpose.safetensors",
    "model_hash": "6f4322fb22",
    "sampler_name": "DPM++ 2M Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 80,
    "cfg_scale": 5,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.5,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 10,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1727241691146-5c56ef36-3f4e-4071-8819-5fc2af755aa9.png)

### 男童写真——海贼王
```plain
{
    "prompt": "masterpiece, best quality,HDR,Monkey D Luffy,(pirate ship on the sea:1.4),<lora:ElementFireSDXL:1.3>,ElementFire,1boy,solo,upper body,(wearing a straw hat:1.2),red jacket,looking at viewer,(serious emotion,seriously,solemn:1.3),muscular physique,(Rough waves whirlpool in the background:1.4),Surrounded by firelight and waves,background blur,focus on the character, Bright colors,high contrast lighting ,<lora:One_Piece_XL:0.8>,luffy,8k resolution, cinematic film still style, <lora:PerfectEyesXL:0.8>,perfecteyes",
    "negative_prompt": "(smile,grip,laughing,mouth open:1.3),Naked,nsfw，Cross-eyed,censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers,bad arms,bad body proportions,pot,broken",
    "model_name": "Nuclear General Purpose.safetensors",
    "model_hash": "6f4322fb22",
    "sampler_name": "DPM++ 2M Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 65,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.5,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1728444225058-7b5350c8-bcb7-411c-bb77-6b9053bb549d.png)

### 女童写真——白雪公主
```plain
{
    "prompt": "masterpiece, best quality,  <lora:Snow White v3:0.8>,Snow White, elegant pose,<lora:Fairy_Style_SDXL:0.95>,ais-fairy,1girl,A red bow is tied in the hair,upper body, (looking at viewer:1.2),magic garden background,a cute rabbit in the background,Lamps and bumbles are hung on trees,sunlight , colorful Flowers,glowing butterflies, (background blur:1.4), <lora:StS_age_slider_v1_initial_release:-2>, <lora:鲜创一派@Lady Hand_SDXL:0.8>,XCYP Lady Hand,Lady Hand",
    "negative_prompt": "Naked,nsfw，Cross-eyed,censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers,bad arms,bad body proportions,pot,broken",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "d6a48d3e20",
    "sampler_name": "Euler a",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 25,
    "cfg_scale": 2,
    "seed": 1826139752,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.7,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1728541760231-7a0d63c4-989b-4142-a666-ac45a8e1a52f.png)

### 女童写真——哈利波特
```plain
{
    "prompt": "masterpiece, best quality,<lora:EnvyGothicRoseXL01:1>,gothic alleyway,(a towering gothic castle in the distant,intricate clock tower:1.4),1girl, solo, white shirt, black robe,(looking at viewer:1.3), <lora:Particles_Style_SDXL:1>,Holding a magic wand in hand ,with wand glowing and ais-particlez emanating in a dazzling array of colors, enveloping the entire scene,surrounded by light and particles, <lora:harry_potter_v1:1>,gryffindor uniform|slytherin uniform|hufflepuff uniform|ravenclaw uniform,<lora:StS_age_slider_v1_initial_release:-1>,<lora:HandFineTuning_XL:0.7>,(pink sky background:1.4)",
    "negative_prompt": "Naked,nsfw,mouth open，(multiple girls:1.5),low quality, blur,bllurry,shaded face, Cross-eyed,censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers,bad arms,bad body proportions,pot,broken",
    "model_name": "Nuclear General Purpose.safetensors",
    "model_hash": "6f4322fb22",
    "sampler_name": "DPM++ SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 65,
    "cfg_scale": 3,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.5,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1728700241079-9b658514-502a-4df6-b854-18b223ed551d.png)

### 男童写真——哈利波特
```plain
{
    "prompt": "masterpiece, best quality, <lora:EnvyGothicRoseXL01:1>,gothic alleyway,(a towering gothic castle in the distant,intricate clock tower:1.5),1boy, solo, white shirt, black robe,(looking at viewer:1.3), <lora:Particles_Style_SDXL:0.9>,(Holding a magic wand in hand:1.2) ,with wand glowing and ais-particlez emanating in a dazzling array of colors, enveloping the entire scene,surrounded by light and particles, <lora:harry_potter_v1:1>,gryffindor uniform|slytherin uniform|hufflepuff uniform|ravenclaw uniform,<lora:StS_age_slider_v1_initial_release:-1>,<lora:HandFineTuning_XL:0.7>,(blue sky background:1.5)",
    "negative_prompt": "Naked,nsfw,mouth open，(multiple boys:1.5),low quality, blur,bllurry,shaded face, Cross-eyed,censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers,bad arms,bad body proportions,pot,broken",
    "model_name": "Nuclear General Purpose.safetensors",
    "model_hash": "6f4322fb22",
    "sampler_name": "DPM++ SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 65,
    "cfg_scale": 3,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.5,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1728700241079-9b658514-502a-4df6-b854-18b223ed551d.png)

### 女童写真——辛德瑞拉
```plain
{
    "prompt": "masterpiece, best quality,Blue tones,<lora:Flower Gate_SDXL:1>,Flower gate AND blue roses,1girl,solo,golden hair,Coiled hair, (Lift the skirt with both hands:1.2),smile,Surrounded by fireflies and feathers, <lora:Cinderella1024:0.7>,Cinderella1024,elegant pose,Luminous moon in night sky ,majestic fairytale castle backdrop,Dark wooden staircase with ornate railings, bathed in soft magical light,focus on character,clouds, (background blur:1.3),cinematic, whimsical, fairy godmother magic,royal ballroom, evening scene, moonlight, fantasy,<lora:StS_age_slider_v1_initial_release:-2>,<lora:HandFineTuning_XL:0.7>,high contract",
    "negative_prompt": "Naked,nsfw,(mouth open,Teeth exposed:1.5)，(multiple girls:1.5),low quality, blur,bllurry,shaded face, Cross-eyed,censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers,bad arms,bad body proportions,pot,broken",
    "model_name": "Nuclear General Purpose.safetensors",
    "model_hash": "6f4322fb22",
    "sampler_name": "DPM++ 2M Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 13,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.5,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1728700241079-9b658514-502a-4df6-b854-18b223ed551d.png)

### 男童写真——小王子
```plain
{
    "prompt": "masterpiece, best quality,1boy,solo,green top BREAK yellow scarf,standing ,Holding a beautiful rose in his hand,(Red petals flutter in the air:1.1) BREAK (a beautiful giant and large ornate crescent moon sculpture behind the boy landing on the sand , Yellow flood,Located in the center of the frame,a fox:1.5) ,(Desert background:1.2),background blur,evening,night, starry sky,high contract,Close-up shots,50mm lens,<lora:Particles_Style_SDXL:1>,ais-particlez,<lora:StS_age_slider_v1_initial_release:-1> ,<lora:HandFineTuning_XL:0.8>",
    "negative_prompt": "Naked,nsfw,(multiple moons:1.5), (mouth open,Teeth exposed:1.5)，(multiple boys:1.5),low quality, blur,bllurry,shaded face, Cross-eyed,censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers,bad arms,bad body proportions,pot,broken,multiple feet,multiple hands",
    "model_name": "Nuclear General Purpose.safetensors",
    "model_hash": "6f4322fb22",
    "sampler_name": "DPM++ 3M SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 25,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.5,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1729070893642-8d836e94-7dff-42c4-bd90-d3e77d336c32.png)

### 摄影照——香港街头
```plain
{
    "prompt": "masterpiece, best quality,Hong Kong style,Wong Kar Wai style,Retro picture quality,(red blur light tone:1.2), 1girl,solo,makeup,lipstick,earings,Face the camera, (looking at viewer:1.4),elegant pose,Charming,<lora:fashion-dress:0.8>, Red velvet dress,Long black wavy hair,hair is blown by the wind,(busy wide street background,The car travels horizontally,Luminous plaque, bustling urban environment:1.3),night,evening, background blur,inspired by contemporary street style and editorial fashion photography,warm lighting,shallow depth of field, 35mm lens, <lora:HandFineTuning_XL:0.6>,blur,blurry,Shoot horizontally,<lyco:EnvyFocalBlurXL01_bokeh:0.9>,bokeh ,<lora:复古港式:1>,LJF_wangjiawei_V1",
    "negative_prompt": "Naked,nsfw, (mouth open,Teeth exposed:1.5)，(multiple girls:1.5), Cross-eyed,censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers,bad arms,bad body proportions,pot,broken,multiple feet,multiple hands",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "d6a48d3e20",
    "sampler_name": "Euler a",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 6,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.5,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1.4,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1729236857107-38c57bfc-eb90-4e3a-9e9b-733cc2c82353.png)





### 摄影照——小清新人像
```plain
{
    "prompt": "okuyama style,1 girl with flowers in front of her face,Foreground flowers, perfect eyes,beautiful eyes,makeup,  beautiful dress,solo,realistic,photorealistic,light and shadow, masterpiece,blurry,(close up), <lora:okuyama:1>",
    "negative_prompt": "Naked,nsfw,(multiple heads:1.5), Cross-eyed,censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers,bad arms,bad body proportions,pot,broken,multiple feet,multiple hands",
    "model_name": "realvisxlV40_v40LightningBakedvae.safetensors",
    "model_hash": "d6a48d3e20",
    "sampler_name": "Euler_Smea_Dy",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 25,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.5,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1729734835088-868d4367-cfa1-497c-ba0a-11facab35c2d.png)

### 摄影照——超现实主义
```plain
{
    "prompt": "masterpiece, best quality,illustration, <lora:HandFineTuning_XL:0.6> ,<lora:franck-bohbot-sdxl-v1-000044:0.7>, <lora:jimmy-marble-v1-000030:0.8>,a photo, 1girl,solo,Fashionable jacket,elegant pose,looking at viewer, makeup, lipstick, standing BREAK (Surrounded by colorful smoke:1.2), A volcano (erupting with colorful smoke:1.2) in the background,desert background,Bright colors, in the style of franck-bohbot,in the style of jimmy-marble, Shoot horizontally,blur,blurry",
    "negative_prompt": "Naked,nsfw, (mouth open,Teeth exposed:1.5)，(multiple girls:1.5), Cross-eyed,censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers,bad arms,bad body proportions,pot,broken,multiple feet,multiple hands",
    "model_name": "Nuclear General Purpose.safetensors",
    "model_hash": "6f4322fb22",
    "sampler_name": "DPM++ SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 20,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.5,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1729734820771-896b623b-649c-4819-83bf-480540e69bba.png)

### 摄影照——维多利亚人像
```plain
{
    "prompt": "masterpiece, best quality, regal and dignified,soft lighting, muted colors,A regal portrait of Queen Victoria, exuding poise and dignity, <lora:旧照片风格:0.7>, 1girl ,solo,elegant pose,necklace, Cross her hands ,crown on head,Coiled hair, <lora:victoria dress:0.8>,hoopdress,Gorgeous,<lora:HandFineTuning_XL:0.6> ,green leaves and flowers in background,gradient background,smooth brushstrokes, detailed rendering of fabrics and jewels,bright colors,high contract",
    "negative_prompt": "Naked,nsfw, (mouth open,Teeth exposed:1.5)，(multiple girls:1.5), watermark,logo,text,censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers,bad arms,bad body proportions,pot,broken,multiple feet,multiple hands",
    "model_name": "Nuclear General Purpose.safetensors",
    "model_hash": "6f4322fb22",
    "sampler_name": "DPM++ 2M Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 25,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.5,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1729734579996-265f6dcc-3a54-44f6-bb43-047e9fa9a1ce.png)

### 女童写真——花架秋千
```plain
{
    "prompt": "masterpiece, best quality, semi-realistic,magic,realistic, 1gir,solo,sitting on a beautiful swing,(float in the air:1.2),smile,lolita dress BREAK garden background,surrounded by butterfies,(colorful buterflies:1.2), sunlight, <lora:StS_age_slider_v1_initial_release:-2>, <lora:Flower Gate_SDXL:0.8>,Flower gate background ,<lora:MJ52:0.8>, <lora:HandFineTuning_XL:0.7> ,<lora:Long_hair_SDXL:0.6>,long hair,wavy hair",
    "negative_prompt": "Naked,nsfw,bad butterflies,broken，(multiple girls:1.5), Cross-eyed,censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands,bad legs, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers,bad arms,bad body proportions,pot,multiple feet,multiple hands",
    "model_name": "Nuclear General Purpose.safetensors",
    "model_hash": "6f4322fb22",
    "sampler_name": "DPM++ 2M Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 15,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.52,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1729752633367-df1aea80-57e0-4e2d-89c6-62a144d0309d.png)

### 男童写真——花与少年杂志封面
```plain
{
    "prompt": "masterpiece, best quality,HDR, photography,portrait,cinematic light and shadow effects,<lora:sunlight_str1-SDXL_v1-dim64-steps1691:1>,sunlight_str1,sunlight from a window,<lora:VOGUE_Fashion_Magazine_Cover_Vintage_1960-1975_SDXL:1.3>,Vogue,editorial,big title text, English text, Colored text, 1boy,solo,wearing white suit,looking at viewer,elegant pose,handsome pose,surrounded by white roses,indoor, green wall,focus on the character's face and the flowers,High contrast, Bright picture,<lora:StS_age_slider_v1_initial_release:-1>, <lora:HandFineTuning_XL:0.7>",
    "negative_prompt": "Naked,nsfw, (mouth open,Teeth exposed:1.5),corner background,(multiple boys:1.5), Cross-eyed,censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers,bad arms,bad body proportions,pot,broken,multiple feet,multiple hands",
    "model_name": "Nuclear General Purpose.safetensors",
    "model_hash": "6f4322fb22",
    "sampler_name": "DPM++ 3M SDE",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 10,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.3,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1.3,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1730108630714-5d79ea4c-380b-4eba-ac6e-a14a94a7ab5a.png)

### 女童写真——金鱼少女
```plain
{
    "prompt": "masterpiece, best quality, realistic, Portrait photography,<lora:sunlight_str1-SDXL_v1-dim64-steps1691:1.1>,sunlight_str1,variegated lighting,1girl,solo,<lora:Long_hair_SDXL:0.7>,long hair,massive hair,Two braids,sitting behind a large aquarium filled with goldfish,(Goldfish swimming playfully in front of her:1.2),indoor, background blur, muted colors, focus on the girl and the goldfish, shallow depth of field, 50mm lens, <lora:StS_age_slider_v1_initial_release:-1>, <lora:okuyama:0.8>,okuyama style,photorealistic,blurry, <lora:MJ52:0.6>",
    "negative_prompt": "Naked,nsfw, (mouth open,Teeth exposed:1.5),corner background,(multiple girls:1.5),smile, laugh, Cross-eyed,censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers,bad arms,bad body proportions,pot,broken,multiple feet,multiple hands",
    "model_name": "Nuclear General Purpose.safetensors",
    "model_hash": "6f4322fb22",
    "sampler_name": "DPM++ 2M Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 10,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.3,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1.3,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1730191993718-d6d2b256-b288-4dc1-9a55-7a3b6560e0b3.png)

### 写真——金鱼少女
```plain
{
    "prompt": "masterpiece, best quality, realistic, Portrait photography,<lora:sunlight_str1-SDXL_v1-dim64-steps1691:1.1>,sunlight_str1,variegated lighting,1girl,solo,<lora:Long_hair_SDXL:0.7>,long hair,massive hair,Two braids,sitting behind a large aquarium filled with goldfish,(Goldfish swimming playfully in front of her:1.2),indoor, background blur, muted colors, focus on the girl and the goldfish, shallow depth of field, 50mm lens, <lora:okuyama:0.8>,okuyama style,photorealistic,blurry, <lora:MJ52:0.6>",
    "negative_prompt": "Naked,nsfw, (mouth open,Teeth exposed:1.5),corner background,(multiple girls:1.5),smile, laugh, Cross-eyed,censored, deformed, bad anatomy, disfigured, poorly drawn face,multiple heads, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers,bad arms,bad body proportions,pot,broken,multiple feet,multiple hands",
    "model_name": "Nuclear General Purpose.safetensors",
    "model_hash": "6f4322fb22",
    "sampler_name": "DPM++ 2M Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 10,
    "cfg_scale": 2,
    "seed": -1,
    "height": 924,
    "width": 620,
    "clip_skip": 1,
    "vae": "sdxl_vae.safetensors",
    "restore_faces": true,
    "hires_options": {
        "enable_hr": true,
        "denoising_strength": 0.3,
        "hr_scale": 2,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 8,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_prompt": "",
        "hr_negative_prompt": ""
    },
    "controlnets": [
        {
            "enable": true,
            "preprocessor": "InsightFace (InstantID)",
            "controlnet_model": "ip-adapter_instant_id_sdxl [eb2d3ec0]",
            "control_weight": 1.3,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "Balanced",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        },
        {
            "enable": true,
            "preprocessor": "instant_id_face_keypoints",
            "controlnet_model": "control_instant_id_sdxl [c5c25a50]",
            "control_weight": 1,
            "input_image": {
                "image_url": ""
            },
            "resize_mode": "Crop and Resize",
            "control_mode": "My prompt is more important ",
            "pixel_perfect": true,
            "starting_steps": 0,
            "ending_steps": 1,
            "threshold_a": 0.5,
            "threshold_b": 0.5
        }
    ]
}



```

![](https://cdn.nlark.com/yuque/0/2024/png/2792817/1730191993718-d6d2b256-b288-4dc1-9a55-7a3b6560e0b3.png)

