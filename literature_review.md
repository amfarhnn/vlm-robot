# CHAPTER 2

# LITERATURE REVIEW

## 2.1 Introduction

This chapter reviews previous research related to `Prompt Engineering for Mobile Robot Navigation`. The project focuses on how natural language instructions can be transformed into navigation goals or actions for a mobile robot using large language models (LLMs), vision-language models (VLMs), and visual navigation models. The review is centered on `LM-Nav: Robotic Navigation with Large Pre-Trained Models of Language, Vision, and Action` by Shah et al. (2023a), which is used as the main baseline paper for this project.

Mobile robot navigation is traditionally solved using localization, mapping, planning, perception, and control. These methods are effective when the navigation goal is provided in a robot-friendly form, such as a coordinate, waypoint, map location, or goal image. However, human users usually communicate navigation goals in natural language. A user may say "go to the chair near the table," "pass the door and stop beside the window," or "move toward the hallway and turn left." These instructions require language understanding, visual grounding, spatial reasoning, and motion execution.

Recent progress in LLMs and VLMs has made natural language navigation more practical. LLMs can extract landmarks, infer intent, decompose instructions, and produce structured plans. VLMs can connect text concepts to visual observations. Visual navigation models can then execute movement toward a selected goal. This creates a new research direction in which robot navigation is not only a planning and control problem, but also a language grounding and prompt engineering problem.

The literature in this chapter is organized around the `LM-Nav` pipeline. `LM-Nav` uses GPT-3 to extract landmarks from an instruction, CLIP to ground those landmarks in visual observations, and ViNG to navigate toward the selected visual goal (Shah et al., 2023a). This modular design is important because it shows that language-guided robot navigation can be built by composing pre-trained models without requiring a large language-annotated robot dataset.

Several later papers improve different parts of the `LM-Nav` idea. `VLMaps` and `HOV-SG` improve spatial grounding by using open-vocabulary maps and hierarchical scene graphs (Huang et al., 2023; Werby et al., 2024). `ViNT` and `NoMaD` improve the navigation execution layer (Shah et al., 2023b; Sridhar et al., 2023). `NaVid`, `Uni-NaVid`, and `NaVILA` represent newer VLM and vision-language-action (VLA) directions (Cheng et al., 2025; Zhang et al., 2024, 2026). `VLMnav` is especially relevant to prompt engineering because it formulates navigation as a question-answering task (Goetting et al., 2024). `VLN-Zero` and `VLM-Nav` provide additional perspectives on zero-shot navigation, memory, and mapless VLM reasoning (Bhatt et al., 2025; Sarker et al., 2026).

The purpose of this literature review is to identify the baseline method, compare related approaches, and define the research gap that motivates this project.

## 2.2 Mobile Robot Navigation and Human Language Interfaces

Mobile robot navigation requires a robot to move from one location to another while avoiding obstacles and maintaining safe behavior. In classical systems, the robot normally relies on a map, localization module, path planner, and controller. The user may provide the target as a coordinate or selected point on a map. This approach is useful in structured environments, but it is not always natural for non-technical users.

Natural language provides a more human-centered interface. Instead of giving a coordinate, a user can describe a target or route using words. This is especially useful in indoor service robots, mobile assistants, warehouse robots, inspection robots, and educational robotics. However, language is difficult for robots because it is often ambiguous and context-dependent. The meaning of "the chair near the table" depends on what the robot can see and how the objects are arranged in the environment.

Language-guided navigation therefore requires three main abilities. First, the system must understand the instruction. Second, it must ground the instruction in the physical environment. Third, it must execute the navigation behavior. These abilities are shown in Figure 2.1.

**Figure 2.1: General language-guided navigation process**

```text
Natural Language Instruction
        |
        v
Language Understanding
        |
        v
Landmark, Goal, or Plan Representation
        |
        v
Vision-Language Grounding
        |
        v
Navigation Goal or Action
        |
        v
Robot Motion Execution
```

The main challenge is that language does not directly correspond to robot motion. An instruction such as "go past the sofa and stop near the door" contains an ordered route, two landmarks, a stopping condition, and an implicit spatial relation. A robot cannot execute this command unless the instruction is converted into an intermediate representation that can be grounded visually and passed to a navigation system.

This is why LLMs and VLMs are increasingly used in robot navigation research. LLMs provide language reasoning, while VLMs provide the ability to connect text to images. The literature reviewed in this chapter studies different ways to combine these models with navigation systems.

## 2.3 Prompt Engineering for Robot Navigation

Prompt engineering is the process of designing input instructions, examples, constraints, and output formats for an LLM or VLM. In robot navigation, prompt engineering is important because the model output must be useful for a downstream robot system. A free-form paragraph is often not enough. The robot may need a structured output such as an ordered landmark list, target object, spatial relation, action label, or navigation constraint.

Prompt engineering can be used in several parts of a robot navigation pipeline. It can extract landmarks from a natural language command, convert an instruction into a list of sub-goals, ask a VLM to identify which image best matches a goal, or ask a VLM to select the next action. The prompt may also require the model to respond in a fixed schema so that the output can be processed automatically.

For this project, prompt engineering is not treated only as a text generation technique. It is treated as an interface between human instruction and robot action. A good prompt should reduce ambiguity, control the model output format, and produce information that can be used by grounding and navigation modules.

**Table 2.1: Roles of prompt engineering in mobile robot navigation**

| Role | Example Output | Purpose |
|---|---|---|
| Landmark extraction | `chair`, `table`, `door` | Identify important objects or places |
| Route decomposition | `door -> hallway -> window` | Convert instruction into ordered sub-goals |
| Spatial relation extraction | `chair near table` | Preserve relation information |
| Constraint extraction | `avoid crowded area` | Identify safety or movement restrictions |
| Visual grounding query generation | `chair near a wooden table` | Improve image-text matching |
| Action selection | `turn left`, `move forward`, `stop` | Support direct navigation decisions |

The reviewed literature shows that prompt engineering becomes more important as robot systems rely more on LLMs and VLMs. In `LM-Nav`, prompting is used to extract landmarks (Shah et al., 2023a). In `VLMaps`, language can be translated into map-based navigation commands (Huang et al., 2023). In `VLMnav`, prompting is used to turn navigation into a question-answering task (Goetting et al., 2024). These examples show that prompt engineering can influence both planning and action selection.

## 2.4 Vision-Language Models and Grounding

Vision-language grounding is the process of connecting text descriptions to visual observations. For mobile robot navigation, this means matching words such as "chair," "door," "hallway," or "exit" with what the robot sees through its camera. Without grounding, a robot may understand the text but still fail to identify the correct target in the environment.

CLIP is one of the most common models used for image-text grounding. It maps images and text into a shared embedding space, allowing similarity comparison between a text query and an image observation. In the context of navigation, a robot can compare a text landmark with candidate images and choose the image that best matches the landmark.

The basic grounding concept can be represented as:

```text
score(image, text) = cosine_similarity(E_image(image), E_text(text))
```

where `E_image` is the image encoder and `E_text` is the text encoder. The image with the highest similarity score is selected as the most relevant visual match.

However, vision-language grounding remains challenging. Objects can be partially visible, visually similar, or absent from the current view. Some instructions also include spatial relations such as "between," "beside," or "near," which are more difficult than recognizing a single object. This motivates later methods such as `VLMaps` and `HOV-SG`, which improve grounding by using spatial maps and scene graphs.

For this project, visual grounding is important because prompt output must eventually connect to the robot's visual world. A prompt that extracts a correct landmark is only useful if the system can ground that landmark in images or environment representations.

Several technical terms are central to this project. A landmark refers to an object, place, or visual cue that can be used as a navigation sub-goal. Grounding refers to the process of matching a language concept with a visual observation or spatial location. A navigation policy refers to the model or algorithm that produces movement decisions. A prompt template refers to the structured instruction given to an LLM or VLM so that the model output can be used by another system module. These terms are important because the proposed research depends on the connection between language interpretation, visual grounding, and navigation execution.

## 2.5 LM-Nav as the Baseline Study

### 2.5.1 Overview of LM-Nav

`LM-Nav: Robotic Navigation with Large Pre-Trained Models of Language, Vision, and Action` by Shah et al. (2023a) is the main baseline paper for this project. The paper was published in the Proceedings of the 6th Conference on Robot Learning, PMLR volume 205, pages 492-504.

The problem addressed by `LM-Nav` is that many visual navigation policies require goals to be specified as images. This is not natural for human users. A human user is more likely to provide a language instruction than a goal image. At the same time, collecting large-scale robot datasets with language annotations is expensive. `LM-Nav` solves this problem by combining pre-trained models instead of training a new language-conditioned navigation model from scratch.

The main idea of `LM-Nav` is to compose three models:

1. GPT-3 extracts landmark names from the natural language instruction.
2. CLIP grounds the extracted landmarks in visual observations.
3. ViNG navigates toward the selected visual landmark.

This pipeline is shown in Figure 2.2.

**Figure 2.2: LM-Nav baseline pipeline**

```text
Language Instruction
        |
        v
GPT-3 Landmark Extraction
        |
        v
Landmark Sequence
        |
        v
CLIP Visual Grounding
        |
        v
Selected Visual Goal
        |
        v
ViNG Navigation Execution
```

### 2.5.2 Methodological Contribution

The key methodological contribution of `LM-Nav` is modular composition. Instead of building one large model that directly maps language and images to robot actions, the system divides the problem into language understanding, visual grounding, and navigation execution. This makes the system easier to interpret and evaluate.

The language component is especially relevant to this project. GPT-3 is prompted to extract landmarks from the instruction. For example, an instruction such as "go past the fountain and toward the library" may be converted into the landmarks `fountain` and `library`. These landmarks become intermediate goals for the navigation system.

The grounding component uses CLIP to match landmark names with visual observations. CLIP provides a way to compare text and images without training a new object detector for every possible landmark. This gives the robot open-vocabulary capability, meaning it can potentially respond to object names that were not part of a fixed detector label set.

The action component uses ViNG, a visual navigation model, to move toward the selected goal. This allows the robot to use a visual navigation policy trained from unannotated trajectory data while still accepting language instructions from the user.

### 2.5.3 Strengths of LM-Nav

`LM-Nav` has several strengths. First, it avoids the need for language-annotated navigation datasets. This is important because collecting robot trajectories with natural language instructions is expensive and time-consuming. Second, it uses pre-trained models that already contain broad language and visual knowledge. Third, its modular structure allows each component to be analyzed separately.

`LM-Nav` is also suitable as a baseline for prompt engineering. The prompt used for landmark extraction directly affects the rest of the pipeline. If the LLM extracts the wrong landmark, the visual grounding and navigation modules will also fail. Therefore, improving prompt design can improve the overall navigation process.

### 2.5.4 Limitations of LM-Nav

Although `LM-Nav` is a strong baseline, it has limitations. The first limitation is that a landmark list may not capture the full meaning of an instruction. Human commands often include spatial relations, constraints, and route order. A simple landmark list may lose important information such as "near the table," "avoid the crowded area," or "after passing the door."

The second limitation is visual grounding. CLIP can match text and images, but it may struggle with precise spatial relations and visually similar objects. For example, if there are several chairs in an environment, CLIP may not know which chair is "near the table" unless the relation is represented clearly.

The third limitation is navigation execution. The final performance depends on the visual navigation model. If the navigation model cannot reach the selected image goal safely, the language and grounding stages are not enough.

These limitations motivate the need to review later work on spatial grounding, stronger navigation backbones, VLM-based action selection, and integrated VLA models.

## 2.6 Spatial Grounding Methods

### 2.6.1 Importance of Spatial Grounding

Spatial grounding is the ability to connect language to locations, objects, and relations in the environment. `LM-Nav` grounds language using image-text matching, but later methods show that maps and scene graphs can provide stronger grounding. This is important because mobile robot navigation often requires spatial reasoning, not only object recognition.

For example, the instruction "go to the chair near the table" requires the robot to identify a chair, a table, and the relation between them. The instruction "go to the kitchen on the second floor" requires a hierarchy of floors and rooms. A simple image-text similarity score may not be enough for these cases.

### 2.6.2 VLMaps

`VLMaps: Visual Language Maps for Robot Navigation` by Huang et al. (2023) proposes an open-vocabulary map representation for robot navigation. Instead of matching language only to individual images, VLMaps stores visual-language features in a map. The robot can then query the map using natural language.

This method is relevant to `LM-Nav` because it improves the grounding stage. In `LM-Nav`, CLIP is used to connect landmarks to visual observations. In `VLMaps`, visual-language features are connected to physical map locations. This allows the robot to answer queries such as where a particular object or region is located.

VLMaps also uses language models to help convert user commands into executable navigation behavior. This makes it relevant to prompt engineering because the language model output can become a structured command for map querying and navigation.

The advantage of VLMaps is that it combines semantic flexibility with spatial structure. It supports open-vocabulary queries while maintaining a map representation. The limitation is that it requires map construction and sensing support, which may make implementation more complex than the simpler `LM-Nav` pipeline.

### 2.6.3 HOV-SG

`HOV-SG: Hierarchical Open-Vocabulary 3D Scene Graphs for Language-Grounded Robot Navigation` by Werby et al. (2024) extends spatial grounding by using hierarchical 3D scene graphs. The method organizes the environment into floors, rooms, and objects. This is useful for long-horizon navigation where instructions refer to large spaces or hierarchical locations.

Compared with `LM-Nav`, HOV-SG provides a richer world representation. `LM-Nav` can identify landmarks, but it does not explicitly model the relationship between floors, rooms, and objects. HOV-SG can support queries that require hierarchy, such as finding an object inside a particular room or on a particular floor.

HOV-SG is important for this project because it shows how language grounding can move beyond image matching. Prompt engineering can produce structured queries, and the scene graph can support grounding and planning. However, HOV-SG also requires more complex perception, mapping, segmentation, and graph construction. It is therefore more suitable as a future improvement direction than as the first implementation target.

### 2.6.4 Summary of Spatial Grounding Works

VLMaps and HOV-SG both address a weakness in `LM-Nav`: limited spatial representation. They show that language-guided navigation can benefit from grounding methods that store semantic information in maps or graphs. For this project, these papers support the idea that prompt outputs should include more than object names. The prompt should also preserve spatial relations, route order, and constraints so that future grounding modules can use them effectively.

**Table 2.2: Spatial grounding papers**

| Paper | Grounding Representation | Relevance to This Project |
|---|---|---|
| `LM-Nav` | CLIP image-text matching | Baseline visual grounding method |
| `VLMaps` | Open-vocabulary visual-language map | Improves grounding with map locations |
| `HOV-SG` | Hierarchical 3D scene graph | Improves grounding with rooms, floors, and objects |

## 2.7 Navigation and Action Models

### 2.7.1 Role of Navigation Models

Language understanding and grounding are not enough to complete robot navigation. The robot must still move toward the target. The navigation model must handle obstacles, visual changes, route uncertainty, and real-world movement constraints. Therefore, improvements in visual navigation models are important for any language-guided navigation system.

In `LM-Nav`, the navigation execution module is ViNG. Later papers such as `ViNT` and `NoMaD` provide stronger alternatives for the action and navigation layer.

### 2.7.2 ViNT

`ViNT: A Foundation Model for Visual Navigation` by Shah et al. (2023b) proposes a transformer-based visual navigation model trained across diverse datasets and robot platforms. The paper argues that visual navigation can benefit from a foundation model approach, where a general model is trained on broad data and then adapted to specific tasks.

ViNT is relevant because it can improve the navigation execution stage of an `LM-Nav`-style system. Instead of relying on an older visual navigation policy, a stronger visual navigation backbone could be used after the language and grounding modules identify the target.

The main strength of ViNT is generalization. Navigation systems must operate across different environments, camera views, lighting conditions, and robot platforms. A foundation navigation model is expected to be more robust than a narrow model trained for a limited setting.

For this project, ViNT is not the main prompt engineering reference, but it is important as a navigation execution reference. It shows that even if prompt extraction and grounding are correct, the final robot performance still depends on the quality of the navigation model.

### 2.7.3 NoMaD

`NoMaD: Goal Masking Diffusion Policies for Navigation and Exploration` by Sridhar et al. (2023) introduces a diffusion-based policy for navigation and exploration. It addresses the challenge of moving toward a goal while also exploring unknown environments. This is important because a robot may not always see the target landmark immediately.

NoMaD is relevant to `LM-Nav` because the baseline assumes that a grounded visual goal can be selected and reached. In real environments, the robot may need to search for a target or explore before the target becomes visible. NoMaD provides a stronger action model for cases where exploration and goal-directed navigation must be combined.

The main advantage of NoMaD is that diffusion policies can represent multiple possible action paths. This is useful in navigation because there may be several valid routes or exploratory directions. For this project, NoMaD supports the discussion that navigation execution is a separate research challenge from prompt design.

### 2.7.4 Summary of Navigation Model Works

ViNT and NoMaD improve the execution side of language-guided navigation. They are not primarily prompt engineering papers, but they are necessary to understand the complete system. A well-designed prompt can produce a good target, but a weak navigation policy may still fail to reach it.

**Table 2.3: Navigation model papers**

| Paper | Main Contribution | Relevance to This Project |
|---|---|---|
| `ViNG` in `LM-Nav` | Visual goal navigation | Baseline navigation execution |
| `ViNT` | Foundation model for visual navigation | Stronger visual navigation backbone |
| `NoMaD` | Diffusion policy for navigation and exploration | Improved exploration and goal-reaching behavior |

## 2.8 VLM and VLA Navigation

### 2.8.1 Shift Toward Integrated Models

The `LM-Nav` pipeline is modular. It separates language understanding, grounding, and navigation. Newer methods move toward more integrated VLM and VLA systems, where a model can process visual observations, language instructions, and action choices together. These systems aim to reduce the separation between perception, reasoning, and action.

This direction is important because navigation is sequential. A robot observes the world over time, remembers what it has seen, and chooses the next movement. Video-based VLMs and VLA models are designed to handle this kind of temporal information.

### 2.8.2 NaVid

`NaVid: Video-based VLM Plans the Next Step for Vision-and-Language Navigation` by Zhang et al. (2024) uses video observations and language instructions to plan the next navigation step. Unlike `LM-Nav`, which extracts landmarks and grounds them separately, NaVid uses a video-based VLM to reason about the navigation situation.

The main improvement of NaVid is the use of temporal visual context. A robot's current decision depends not only on the current frame but also on what it has seen before. Video history helps the system understand progress through the environment.

For this project, NaVid is relevant as a later-stage VLM navigation direction. It shows that VLMs can be used not only for grounding, but also for next-step decision making. However, because this project focuses on prompt engineering and modular navigation, NaVid is used mainly as a supporting reference rather than the baseline method.

### 2.8.3 Uni-NaVid

`Uni-NaVid: A Video-based Vision-Language-Action Model for Unifying Embodied Navigation Tasks` by Zhang et al. (2026) is listed in the RSS 2026 program. It represents a newer direction where one VLA model is designed to support several embodied navigation tasks, including instruction following, object search, tracking, and embodied question answering.

Uni-NaVid is important because it suggests that future navigation systems may not be limited to one task type. Instead, one model may handle different navigation-related tasks using a shared visual-language-action representation.

Compared with `LM-Nav`, Uni-NaVid is more integrated and likely requires larger training resources. This makes it less suitable as the first implementation for this project, but valuable as a future research direction.

### 2.8.4 NaVILA

`NaVILA: Legged Robot Vision-Language-Action Model for Navigation` by Cheng et al. (2025) focuses on VLA navigation for legged robots. It uses a high-level VLA model to generate movement commands, while a lower-level locomotion policy handles physical execution. This separation is important because high-level reasoning and low-level control operate at different levels.

NaVILA is relevant because it shows how language and visual reasoning can be connected to real robot motion. It also supports the idea of using structured intermediate actions. For example, the VLA model may decide a movement direction or mid-level command, while the locomotion controller handles the detailed movement.

For this project, NaVILA is a useful reference for future physical robot implementation. It shows that prompt-like structured outputs can become a bridge between reasoning models and robot control.

### 2.8.5 Summary of VLM and VLA Works

NaVid, Uni-NaVid, and NaVILA show that the field is moving toward more integrated navigation agents. These methods improve on the modular `LM-Nav` design by allowing vision, language, and action to interact more directly. However, they may be harder to reproduce because they require large datasets, specialized models, or real robot experiments.

**Table 2.4: VLM and VLA navigation papers**

| Paper | Main Direction | Relevance to This Project |
|---|---|---|
| `NaVid` | Video-based VLM next-step planning | Supports VLM-based navigation reasoning |
| `Uni-NaVid` | Unified VLA navigation tasks | Represents latest integrated model direction |
| `NaVILA` | VLA navigation for legged robots | Shows connection between VLA reasoning and real robot movement |

## 2.9 Prompt-Based and Zero-Shot Navigation

### 2.9.1 VLMnav

`VLMnav: End-to-End Navigation with Vision Language Models: Transforming Spatial Reasoning into Question-Answering` by Goetting et al. (2024) is highly relevant to this project because it directly studies prompt-based navigation. The paper formulates navigation as a question-answering task for a VLM. Instead of only extracting landmarks, the model is asked to choose navigation actions based on visual observations and language goals.

This approach is important because it moves prompt engineering closer to the action selection stage. In `LM-Nav`, the prompt asks the LLM to identify landmarks. In `VLMnav`, the prompt can ask the VLM which action should be taken next. This creates a direct relationship between prompt design and navigation behavior.

For this project, VLMnav provides the strongest prompt-engineering reference after `LM-Nav`. It supports the idea that different prompt templates can be compared experimentally. For example, a project can compare a landmark extraction prompt, a structured output prompt, and an action question-answering prompt.

### 2.9.2 VLN-Zero

`VLN-Zero: Rapid Exploration and Cache-Enabled Neurosymbolic Vision-Language Planning for Zero-Shot Transfer in Robot Navigation` by Bhatt et al. (2025) focuses on zero-shot navigation, exploration, memory, and efficient planning. It combines VLM-guided exploration with symbolic scene graphs and caching.

VLN-Zero is relevant because one limitation of VLM-based navigation is repeated model calling. If a robot asks a large model for every small action, the system may become slow or expensive. VLN-Zero addresses this by building reusable memory and caching useful trajectories.

Compared with `LM-Nav`, VLN-Zero places more emphasis on exploration and memory. This is useful for future work because a mobile robot may need to explore before it can ground a target landmark. It also shows that prompt engineering can be used not only for instruction parsing, but also for guiding exploration and building structured memory.

### 2.9.3 VLM-Nav for UAV Navigation

`VLM-Nav: Mapless UAV Navigation Using Monocular Vision Driven by Vision-Language Models` by Sarker et al. (2026) is a recent paper that studies VLM-based UAV navigation. The system uses monocular vision, zero-shot depth estimation, and VLM reasoning for obstacle-aware mapless navigation.

This paper is less directly related to `LM-Nav` because it focuses on UAV navigation rather than language-guided ground robot navigation. However, it is useful as a recent example of VLMs being used for navigation reasoning. It shows that VLMs can support obstacle interpretation, scene understanding, and motion-related decisions without requiring a full prebuilt map.

For this project, VLM-Nav is considered a supporting reference. It strengthens the motivation that VLMs are becoming important in robot navigation, but the main methodology remains closer to `LM-Nav` and `VLMnav`.

### 2.9.4 Summary of Prompt-Based and Zero-Shot Works

VLMnav, VLN-Zero, and VLM-Nav show different ways to use VLMs in navigation. VLMnav focuses on action selection through question answering. VLN-Zero focuses on zero-shot exploration, memory, and symbolic planning. VLM-Nav focuses on mapless UAV navigation using monocular visual reasoning.

**Table 2.5: Prompt-based and zero-shot navigation papers**

| Paper | Main Contribution | Relevance to This Project |
|---|---|---|
| `VLMnav` | Navigation as VLM question answering | Main prompt-engineering improvement reference |
| `VLN-Zero` | Zero-shot VLM planning with memory and caching | Supports efficient exploration and reuse |
| `VLM-Nav` | Mapless UAV navigation with VLM reasoning | Recent supporting example of VLM navigation |

## 2.10 Comparative Review of Related Works

The reviewed papers can be compared based on which part of the navigation pipeline they improve. `LM-Nav` is the main baseline because it provides a complete modular pipeline. The other papers improve specific weaknesses of the baseline.

**Table 2.6: Comparison of related papers**

| Paper | Main Focus | Strength | Limitation |
|---|---|---|---|
| `LM-Nav` | Landmark extraction, CLIP grounding, visual navigation | Clear modular baseline using pre-trained models | Landmark-only representation may lose spatial details |
| `VLMaps` | Open-vocabulary spatial maps | Stronger grounding with map locations | Requires map construction and sensing support |
| `HOV-SG` | Hierarchical 3D scene graphs | Supports rooms, floors, and object hierarchy | More complex pipeline |
| `ViNT` | Visual navigation foundation model | Stronger navigation backbone | Does not focus on prompt engineering |
| `NoMaD` | Diffusion policy for navigation and exploration | Handles exploration and goal reaching | Requires navigation data and policy deployment |
| `NaVid` | Video-based VLM navigation | Uses temporal context for next-step planning | More integrated and harder to reproduce |
| `Uni-NaVid` | Unified VLA navigation tasks | Supports multiple embodied tasks | Recent and resource-intensive |
| `NaVILA` | VLA navigation for legged robots | Connects VLA reasoning to real locomotion | Focuses on legged robots rather than general mobile robots |
| `VLMnav` | Prompt-based action selection | Strong prompt-engineering relevance | Direct VLM actions may need safety validation |
| `VLN-Zero` | Zero-shot planning and memory | Reduces repeated model calls using caching | More complex than a basic LM-Nav pipeline |
| `VLM-Nav` | Mapless UAV navigation | Recent VLM navigation example | UAV domain differs from ground mobile robot navigation |

The comparison shows that no single paper solves all aspects of prompt-engineered mobile robot navigation. `LM-Nav` provides the clearest baseline, but it can be improved by later methods. `VLMaps` and `HOV-SG` improve spatial grounding. `ViNT` and `NoMaD` improve navigation execution. `NaVid`, `Uni-NaVid`, and `NaVILA` represent future integrated VLM/VLA navigation systems. `VLMnav` provides the most direct support for prompt-based action selection.

From a critical perspective, the papers can be divided into methods that are practical for immediate implementation and methods that are more suitable as future extensions. `LM-Nav` and `VLMnav` are most suitable for this project because both can be studied through prompt design, structured outputs, and image-based evaluation. `VLMaps` and `HOV-SG` provide stronger grounding, but they require mapping or scene-graph construction. `ViNT` and `NoMaD` improve execution, but they depend on navigation model deployment and training data. Therefore, the project should use `LM-Nav` as the baseline, use `VLMnav` as the main prompt-engineering comparison, and discuss the remaining methods as improvement directions.

The relationship between these papers and the project is summarized in Figure 2.3.

**Figure 2.3: Positioning of related works around LM-Nav**

```text
                         VLM/VLA Navigation
                  NaVid, Uni-NaVid, NaVILA
                                |
                                v
Spatial Grounding -----> LM-Nav Baseline -----> Navigation Execution
VLMaps, HOV-SG          GPT-3 + CLIP + ViNG     ViNT, NoMaD
                                |
                                v
                    Prompt-Based Action Selection
                              VLMnav
```

## 2.11 Research Gap and Motivation

The literature shows that language-guided robot navigation has improved significantly, but several gaps remain.

First, prompt design is still under-analyzed in modular navigation pipelines. `LM-Nav` uses an LLM to extract landmarks, but the effect of different prompt structures is not the main focus of the paper. Since the landmark extraction output affects the entire pipeline, there is a need to study how prompt design changes the quality of extracted navigation information.

Second, landmark extraction alone is not sufficient for many natural language instructions. Human instructions often include spatial relations, route order, constraints, and ambiguous references. A prompt that only extracts object names may lose important information. This creates a need for structured prompt outputs that include landmarks, relations, sub-goals, constraints, and uncertainty.

Third, visual grounding remains a bottleneck. CLIP-based matching is useful, but it may not be enough for relation-based instructions or environments with multiple similar objects. Papers such as `VLMaps` and `HOV-SG` show that maps and scene graphs can improve grounding, but these methods are more complex. A practical project can begin by improving the text representation through prompt engineering before moving toward map-based grounding.

Fourth, navigation execution and prompt reasoning are often studied separately. Papers such as `ViNT` and `NoMaD` improve navigation policies, while papers such as `VLMnav` improve VLM-based decision making. A complete system must connect these components. Therefore, this project is motivated by the need to design prompt outputs that can be used by grounding and navigation modules.

Fifth, evaluation should include more than final navigation success. A prompt-engineered navigation system should also be evaluated based on landmark extraction accuracy, relation extraction accuracy, output format validity, grounding accuracy, action relevance, latency, and failure cases.

Based on these gaps, this project is motivated to study prompt engineering for an `LM-Nav`-style mobile robot navigation pipeline. The main research direction is to improve the extraction of structured navigation goals from natural language instructions and examine how those outputs can support visual grounding and navigation decision making.

**Table 2.7: Research gap synthesis and project strategy**

| Research Gap | Supporting Literature | Project Strategy |
|---|---|---|
| Prompt design is not deeply analyzed in modular navigation pipelines | `LM-Nav`, `VLMnav` | Compare baseline, structured, spatial-reasoning, and action-selection prompts |
| Landmark extraction loses spatial relations and constraints | `LM-Nav`, `VLMaps`, `HOV-SG` | Extract landmarks, ordered sub-goals, relations, constraints, and uncertainty |
| CLIP grounding may struggle with relation-based instructions | `LM-Nav`, `VLMaps`, `HOV-SG` | Test direct landmark grounding against prompt-expanded grounding |
| Navigation execution is often separated from language reasoning | `ViNT`, `NoMaD`, `NaVILA` | Define output formats that can be passed to future navigation policies |
| Evaluation often focuses on final success only | `VLMnav`, `VLN-Zero` | Evaluate extraction accuracy, output validity, grounding accuracy, action relevance, and failure cases |

The main research question can be stated as:

How can prompt engineering improve the extraction of structured navigation goals from natural language instructions for an `LM-Nav`-style mobile robot navigation pipeline?

## 2.12 Chapter Summary

This chapter reviewed research related to prompt engineering for mobile robot navigation. The review began by discussing mobile robot navigation, natural language interfaces, prompt engineering, and vision-language grounding. `LM-Nav` was then reviewed as the main baseline methodology because it combines GPT-3 for landmark extraction, CLIP for visual grounding, and ViNG for navigation execution.

The chapter also reviewed papers that improve different parts of the `LM-Nav` pipeline. `VLMaps` and `HOV-SG` improve spatial grounding through open-vocabulary maps and hierarchical 3D scene graphs. `ViNT` and `NoMaD` improve the navigation execution layer. `NaVid`, `Uni-NaVid`, and `NaVILA` represent newer VLM/VLA navigation directions. `VLMnav` provides an important prompt-engineering reference by formulating navigation as VLM question answering. `VLN-Zero` and `VLM-Nav` provide additional perspectives on zero-shot planning, memory, and mapless VLM navigation.

The literature shows that `LM-Nav` is a suitable baseline for this project, but there is still a research gap in structured prompt engineering for navigation. The next chapter describes the methodology used to design, implement, and evaluate a prompt-engineered mobile robot navigation pipeline.

## REFERENCE

Bhatt, N. P., Yang, Y., Siva, R., Samineni, P., Milan, D., Wang, Z., & Topcu, U. (2025). *VLN-Zero: Rapid exploration and cache-enabled neurosymbolic vision-language planning for zero-shot transfer in robot navigation*. arXiv. https://doi.org/10.48550/arXiv.2509.18592

Cheng, A.-C., Ji, Y., Yang, Z., Gongye, Z., Zou, X., Kautz, J., Biyik, E., Yin, H., Liu, S., & Wang, X. (2025). NaVILA: Legged robot vision-language-action model for navigation. *Proceedings of Robotics: Science and Systems*. https://doi.org/10.15607/RSS.2025.XXI.018

Goetting, D., Singh, H. G., & Loquercio, A. (2024). *End-to-end navigation with vision language models: Transforming spatial reasoning into question-answering*. arXiv. https://doi.org/10.48550/arXiv.2411.05755

Huang, C., Mees, O., Zeng, A., & Burgard, W. (2023). Visual language maps for robot navigation. *Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)*. https://vlmaps.github.io/

Sarker, G. C., Azad, A. K. M., Rahman, S., & Hasan, M. M. (2026). VLM-Nav: Mapless UAV navigation using monocular vision driven by vision-language models. *PLOS One, 21*(4), e0345778. https://doi.org/10.1371/journal.pone.0345778

Shah, D., Osinski, B., Ichter, B., & Levine, S. (2023a). LM-Nav: Robotic navigation with large pre-trained models of language, vision, and action. *Proceedings of the 6th Conference on Robot Learning, Proceedings of Machine Learning Research, 205*, 492-504. https://proceedings.mlr.press/v205/shah23b.html

Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N., & Levine, S. (2023b). ViNT: A foundation model for visual navigation. *Proceedings of the 7th Conference on Robot Learning, Proceedings of Machine Learning Research, 229*, 711-733. https://proceedings.mlr.press/v229/shah23a.html

Sridhar, A., Shah, D., Glossop, C., & Levine, S. (2023). *NoMaD: Goal masked diffusion policies for navigation and exploration*. arXiv. https://arxiv.org/abs/2310.07896

Werby, A., Huang, C., Buchner, M., Valada, A., & Burgard, W. (2024). Hierarchical open-vocabulary 3D scene graphs for language-grounded robot navigation. *Proceedings of Robotics: Science and Systems*. https://doi.org/10.15607/RSS.2024.XX.077

Zhang, J., Wang, K., Xu, R., Zhou, G., Hong, Y., Fang, X., Wu, Q., Zhang, Z., & Wang, H. (2024). NaVid: Video-based VLM plans the next step for vision-and-language navigation. *Proceedings of Robotics: Science and Systems*. https://doi.org/10.15607/RSS.2024.XX.079

Zhang, J., Wang, K., Wang, S., Li, M., Liu, H., Wei, S., Wang, Z., Zhang, Z., & Wang, H. (2026). Uni-NaVid: A video-based vision-language-action model for unifying embodied navigation tasks. *Robotics: Science and Systems 2026 Program*. https://roboticsconference.org/program/papers/13/
