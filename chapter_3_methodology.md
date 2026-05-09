# CHAPTER 3

# RESEARCH METHODOLOGY

## 3.1 Introduction

This chapter presents the methodology for the project `Prompt Engineering for Mobile Robot Navigation`. The project focuses on studying how natural language instructions can be converted into navigation-relevant outputs for a mobile robot using prompt engineering, large language models (LLMs), vision-language models (VLMs), and visual navigation concepts.

The main methodology is based on `LM-Nav: Robotic Navigation with Large Pre-Trained Models of Language, Vision, and Action` by Shah et al. (2023a). `LM-Nav` provides a modular baseline in which an LLM extracts landmarks from language instructions, CLIP grounds those landmarks in visual observations, and a visual navigation model executes movement toward the selected goal. This project adopts the same baseline idea, but places stronger emphasis on prompt engineering and structured navigation outputs.

The methodology also considers later research directions as supporting references. `VLMnav` by Goetting et al. (2024) is used as a reference for prompt-based action selection through question answering. `VLMaps` and `HOV-SG` are used as references for stronger spatial grounding (Huang et al., 2023; Werby et al., 2024). `ViNT` and `NoMaD` are used as references for improved navigation execution (Shah et al., 2023b; Sridhar et al., 2023).

The proposed work is developed as a research prototype. The main objective is not only to produce a navigation output, but also to evaluate how different prompt designs affect the quality of landmark extraction, spatial reasoning, visual grounding, and action or goal selection.

## 3.2 Development Method and Project Workflow

The development process follows an iterative research and prototyping approach. This approach is suitable because the project contains multiple connected modules: language instruction processing, prompt design, landmark extraction, vision-language grounding, navigation decision making, and evaluation. Each module must be tested independently before being combined into a complete pipeline. This methodology is justified by the literature because `LM-Nav` shows that language, vision, and action can be separated into modular components, while later works such as `VLMnav`, `VLMaps`, and `HOV-SG` show that prompt formulation and grounding representations can strongly affect navigation decisions.

### 3.2.1 Methodology Alignment with Research Objectives

The methodology is organized according to three research objectives. Each objective is linked to a specific method, output, and evaluation approach.

**Table 3.1: Methodology Alignment with Research Objectives**

| Research Objective | Method Used | Expected Output | Evaluation |
|---|---|---|---|
| Objective 1: To study an `LM-Nav`-style baseline for language-guided mobile robot navigation | Review `LM-Nav` and define the baseline pipeline | Baseline model flow: LLM landmark extraction, CLIP grounding, navigation execution | Baseline pipeline is clearly described and justified from literature |
| Objective 2: To design prompt templates for extracting structured navigation goals | Develop baseline, structured, spatial-reasoning, and safety-aware prompts | Landmark list, spatial relations, route order, constraints, and uncertainty labels | Output validity, extraction accuracy, and relation accuracy |
| Objective 3: To evaluate whether structured prompt engineering improves the navigation pipeline | Compare prompt outputs and grounding/action results across test instructions | Quantitative scores and qualitative failure analysis | Comparison between baseline prompt and improved prompts |

### 3.2.2 Theoretical Framework

The proposed methodology is based on the relationship between language instruction, prompt design, visual grounding, and navigation decision making. A natural language instruction is represented as `I`, and a prompt template is represented as `P`. The LLM generates a structured navigation representation `R`, as shown in Eq. (3.1).

```text
R = LLM(I, P)                                                    (3.1)
```

The structured representation `R` may include landmarks, target object, route order, spatial relations, constraints, and uncertainty. The grounding module then compares each text goal with candidate visual observations. The similarity score between image `x` and text query `q` is calculated using cosine similarity, as shown in Eq. (3.2).

```text
S(x, q) = cosine_similarity(E_image(x), E_text(q))               (3.2)
```

where `E_image(x)` is the image embedding and `E_text(q)` is the text embedding. The selected target observation `x*` is the candidate image with the highest similarity score, as shown in Eq. (3.3).

```text
x* = argmax S(x_i, q)                                            (3.3)
```

For action-selection experiments inspired by `VLMnav`, the VLM receives the instruction, current observation, and available action choices. The selected action `a*` is represented in Eq. (3.4).

```text
a* = VLM(I, x_current, A)                                        (3.4)
```

where `A` is the fixed action set, such as `move forward`, `turn left`, `turn right`, `stop`, and `search`. These equations provide the theoretical basis for the proposed prompt-engineered navigation pipeline.

### 3.2.3 Overall Project Workflow

The workflow begins with a study of `LM-Nav` and related papers. Based on the literature, a baseline navigation pipeline is defined. Natural language navigation instructions are then prepared and grouped according to instruction type, such as simple landmark goals, ordered landmark routes, spatial relations, and ambiguous instructions. Prompt templates are designed and tested to extract structured navigation information from these instructions.

After the prompt engineering stage, the extracted landmarks or sub-goals are passed to a vision-language grounding module. This module compares text goals with visual observations using CLIP or a VLM-based method. The selected visual goal is then passed to a navigation decision module. Depending on available resources, the final navigation stage may be evaluated using an image sequence, a simulator, or a physical mobile robot.

The complete methodology is summarized in the following workflow.

**Figure 3.1: Proposed project workflow**

```text
Literature Review
        |
        v
Problem Definition and Baseline Selection
        |
        v
Navigation Instruction Preparation
        |
        v
Prompt Template Design
        |
        v
Landmark and Plan Extraction
        |
        v
Is the output valid?
    | yes
    v
Vision-Language Grounding
        |
        v
Is the target grounded?
    | yes
    v
Navigation Goal or Action Selection
        |
        v
Testing, Evaluation, and Analysis
        |
        v
Prompt Improvement and Final Discussion

If output is not valid:
        -> refine prompt template and repeat extraction

If target is not grounded:
        -> expand text query or review candidate observations
```

**Table 3.2: Development Workflow**

| Stage | Activity | Expected Output |
|---|---|---|
| Stage 1 | Review `LM-Nav` and related papers | Baseline method and research gap |
| Stage 2 | Prepare navigation instruction set | List of test instructions |
| Stage 3 | Design prompt templates | Baseline and improved prompts |
| Stage 4 | Extract landmarks and spatial relations | Structured navigation output |
| Stage 5 | Ground extracted goals with visual observations | Selected image goal or target landmark |
| Stage 6 | Select navigation goal or action | Action label, waypoint, or visual goal |
| Stage 7 | Evaluate performance | Quantitative and qualitative results |
| Stage 8 | Improve prompts and analyze failures | Final methodology discussion |

## 3.3 System Requirements, Constraints, and Acceptance Criteria

The project requirements are defined to ensure that the research prototype can be evaluated systematically. Since this project focuses on prompt engineering and navigation reasoning, the main success criteria are related to structured output quality, grounding accuracy, and navigation relevance.

**Table 3.3: Requirements and Acceptance Criteria**

| Requirement | Specification | Verification Method | Pass Criteria |
|---|---|---|---|
| Natural language input | The system accepts human navigation instructions | Instruction input test | Instruction is processed without manual rewriting |
| Landmark extraction | The LLM identifies important landmarks from the instruction | Output comparison with expected labels | Correct landmarks are extracted for most test cases |
| Spatial relation extraction | The prompt captures relations such as near, beside, between, and after | Manual annotation comparison | Spatial relations are represented in structured output |
| Structured output format | The LLM produces consistent machine-readable output | Format validation | Output follows the required schema |
| Visual grounding | Text goals are matched with image observations | Image-text matching test | Correct target image or landmark is selected |
| Navigation decision | The system selects a goal or action based on grounding | Scenario-based evaluation | Decision is relevant to the instruction |
| Prompt comparison | Multiple prompt templates are tested | Experimental comparison | Improved prompt performs better than baseline prompt |
| Logging and analysis | Inputs, prompts, outputs, and errors are recorded | Log inspection | Results can be reviewed and reproduced |

The project also has several constraints. First, the study is limited by the availability of robot hardware, simulation tools, datasets, and model access. Second, the system is not expected to train a new foundation model from scratch. Instead, it uses pre-trained models and prompt engineering. Third, the system must be evaluated carefully because LLM and VLM outputs can be inconsistent across runs.

## 3.4 Overall System Architecture

The proposed system architecture follows the modular design of `LM-Nav`. The system is divided into six main modules: user instruction input, prompt engineering, landmark and plan extraction, vision-language grounding, navigation decision making, and evaluation.

**Figure 3.2: Proposed system architecture**

```text
User Navigation Instruction
        |
        v
Prompt Engineering Module
        |
        v
Landmark and Plan Extraction Module
        |
        v
Structured Navigation Representation
        |
        v
Vision-Language Grounding Module
        |
        v
Selected Landmark, Image Goal, or Region
        |
        v
Navigation Decision Module
        |
        v
Action, Waypoint, or Goal Output
        |
        v
Evaluation and Result Logging
```

The user instruction input module receives a natural language navigation command. The prompt engineering module converts the instruction into a format suitable for an LLM or VLM. The landmark and plan extraction module identifies important landmarks, route order, spatial relations, and constraints. The vision-language grounding module connects the extracted text goals with visual observations. The navigation decision module selects the next goal or action. Finally, the evaluation module records the output and compares it against expected results.

This architecture is intentionally modular. If one module performs poorly, it can be tested and improved separately. For example, if the system selects the wrong target, the error may come from the prompt, the visual grounding module, or the navigation decision module. Modular testing makes the research easier to analyze.

## 3.5 Data and Experimental Materials

The project requires two main types of data: natural language navigation instructions and visual observations. The natural language instructions are used to evaluate prompt engineering. The visual observations are used to evaluate grounding and navigation decision making.

The instruction set should include different levels of difficulty. Simple instructions contain one target landmark. Medium instructions contain multiple landmarks or ordered steps. More complex instructions include spatial relations, constraints, or ambiguous wording.

**Table 3.4: Instruction Categories**

| Category | Example Instruction | Purpose |
|---|---|---|
| Single landmark | "Go to the door." | Test basic landmark extraction |
| Landmark with relation | "Go to the chair near the table." | Test spatial relation extraction |
| Ordered route | "Pass the sofa, then move toward the window." | Test sequence extraction |
| Ambiguous instruction | "Go to the nearest exit." | Test reasoning and uncertainty handling |
| Constraint-based instruction | "Move toward the desk but avoid the crowded area." | Test constraint extraction |
| Action-oriented instruction | "Turn left and move forward until the hallway." | Test action or route interpretation |

The visual observations may be collected from a mobile robot camera, an indoor environment, a simulator, or a set of manually captured images. The minimum requirement is that each test scenario contains candidate images or scene views that include relevant landmarks. If a simulator or robot platform is available, the visual observations can be connected to actual navigation actions. If not, the project can still evaluate the language and grounding components using image-based scenarios.

**Table 3.5: Experimental Materials**

| Material | Function |
|---|---|
| Navigation instruction set | Input for prompt engineering experiments |
| Candidate scene images | Input for visual grounding |
| Expected landmark labels | Ground truth for extraction evaluation |
| Expected target image or region | Ground truth for grounding evaluation |
| Prompt templates | Experimental variables |
| LLM or VLM access | Language reasoning and action selection |
| CLIP or equivalent image-text model | Image-text grounding |
| Result log file | Stores inputs, outputs, scores, and errors |

The implementation is mainly software-based. If a physical mobile robot is available, the same pipeline can be connected to the robot camera and navigation controller. If hardware is not available during FYP1, the methodology can still be validated using image-based scenarios or a simulator because the main focus is prompt engineering and grounding.

**Table 3.6: Software, Model, and Platform Requirements**

| Item | Purpose | Example |
|---|---|---|
| Programming environment | Run the experiment pipeline and store results | Python |
| LLM access | Generate landmark and structured navigation outputs | GPT-style model or local LLM |
| Vision-language model | Ground text goals in image observations | CLIP or modern VLM |
| Dataset or image set | Provide candidate visual observations | Robot camera images, simulator images, or indoor scene images |
| Evaluation spreadsheet or log file | Record outputs, scores, and failure cases | CSV, Markdown table, or spreadsheet |
| Optional simulator | Test navigation decisions without physical hardware | Indoor navigation simulator |
| Optional mobile robot | Test the full pipeline in a real environment | Wheeled mobile robot with camera |

Based on the hardware review in Chapter 2, the proposed project does not need to reproduce the full hardware setup used by every reference paper. `LM-Nav` used a Clearpath Jackal with RGB cameras, GPS, wheel encoders, and an IMU, but the exact onboard computer board was not stated. `ViNT` and `NoMaD` provide the clearest board-level reference for a practical mobile robot setup because the official deployment stack is associated with a LoCoBot and NVIDIA Jetson Orin Nano. `Uni-NaVid` provides a stronger recent VLA hardware reference by using a Unitree Go2, RealSense D455 RGB camera, Unitree LiDAR-L1, portable Wi-Fi, and a remote NVIDIA A100 server. Therefore, the minimum practical setup for this FYP is a laptop or workstation, a curated set of indoor scene images or simulator views, and access to an LLM/VLM. If a physical prototype is available, the preferred hardware is a wheeled mobile robot with a front-facing RGB camera and optional odometry or IMU. An NVIDIA Jetson Orin Nano can be used if onboard visual navigation is required, while RGB-D hardware such as RealSense or Azure Kinect is treated as an extension for spatial mapping rather than a compulsory requirement for the prompt-engineering prototype.

## 3.6 Prompt Engineering Design

Prompt engineering is the main focus of this project. The prompt controls how the LLM or VLM interprets the navigation instruction and how it produces an output that can be used by the navigation pipeline.

Several prompt types are proposed for comparison.

**Table 3.7: Prompt Templates for Evaluation**

| Prompt Type | Description | Expected Output |
|---|---|---|
| Baseline landmark prompt | Extracts only landmark names from the instruction | Ordered landmark list |
| Structured output prompt | Requires a fixed schema for landmarks, relations, and constraints | JSON-style navigation plan |
| Spatial reasoning prompt | Emphasizes object relations and route order | Landmarks with relation labels |
| Safety-aware prompt | Extracts obstacles, forbidden areas, or caution instructions | Goal and safety constraints |
| VLMnav-style question prompt | Asks a VLM to select the best action from choices | Action label with reason |

The structured prompt is expected to produce a consistent output format. A simplified output schema is shown below.

```json
{
  "instruction": "Go to the chair near the table.",
  "landmarks": ["chair", "table"],
  "target": "chair",
  "spatial_relations": [
    {
      "object": "chair",
      "relation": "near",
      "reference": "table"
    }
  ],
  "ordered_subgoals": ["table", "chair"],
  "constraints": [],
  "uncertainty": "low"
}
```

This schema is useful because it gives the navigation system a structured representation instead of free-form text. It also makes evaluation easier because each field can be checked independently.

The main tunable parameters in the prompt engineering experiment are the prompt template, output schema, model temperature, maximum output length, grounding query format, number of candidate images, similarity threshold, and action set. These parameters are important because they can affect output consistency, grounding accuracy, and final navigation decisions.

**Table 3.8: Main Experimental Parameters**

| Parameter | Description | Planned Setting |
|---|---|---|
| Prompt template | Type of prompt used for extraction or action selection | Baseline, structured, spatial-reasoning, safety-aware |
| Output schema | Required format of the LLM output | JSON-style structured output |
| Model temperature | Controls randomness of model output | Low value for consistent output |
| Grounding query | Text query used for image-text matching | Direct landmark or prompt-expanded query |
| Candidate image count | Number of images compared during grounding | Depends on test scenario |
| Similarity threshold | Minimum acceptable grounding score | Tuned during testing |
| Action set | Available movement choices for VLM action selection | Forward, left, right, stop, search |

## 3.7 Landmark and Plan Extraction Module

The landmark and plan extraction module is responsible for converting a natural language instruction into navigation-relevant information. This module follows the main idea of `LM-Nav`, where an LLM is used to extract landmarks from a route instruction.

The input to this module is a navigation command written in natural language. The output is a structured representation containing target landmarks, route order, spatial relations, and constraints. The extracted information is then passed to the visual grounding module.

**Table 3.9: Example of Landmark and Plan Extraction**

| Input Instruction | Expected Structured Output |
|---|---|
| "Go to the chair." | Target: chair |
| "Go to the chair near the table." | Target: chair, relation: near table |
| "Pass the door and stop at the window." | Ordered sub-goals: door, window |
| "Move forward until the hallway, then turn left." | Actions: move forward, turn left; landmark: hallway |
| "Avoid the crowded area and go to the reception desk." | Target: reception desk; constraint: avoid crowded area |

The module will be evaluated based on whether the extracted output matches the intended meaning of the instruction. Errors may include missing landmarks, wrong landmark order, incorrect relation extraction, invalid output format, or hallucinated landmarks not present in the instruction.

## 3.8 Vision-Language Grounding Module

The vision-language grounding module connects extracted text goals to visual observations. This module is based on the CLIP grounding stage in `LM-Nav`. The extracted target landmark is converted into a text query, and candidate images are compared against this query.

The basic grounding score can be represented as:

```text
score(image, text) = cosine_similarity(E_image(image), E_text(text))
```

where `E_image` is the image encoder and `E_text` is the text encoder. The image with the highest similarity score is selected as the most likely target observation.

Prompt engineering can also improve grounding by expanding the text query. For example, instead of using only "chair," the system may use "a chair near a table in an indoor room." This makes the grounding query more descriptive and may improve matching for spatially rich instructions.

**Table 3.10: Grounding Strategies**

| Strategy | Description | Expected Benefit |
|---|---|---|
| Direct landmark grounding | Uses only the target landmark as text query | Simple and close to `LM-Nav` |
| Prompt-expanded grounding | Uses richer text descriptions generated by the LLM | Improves semantic detail |
| Relation-aware grounding | Includes spatial relation in the query | Improves relation-based target selection |
| VLM question grounding | Asks a VLM which image best matches the instruction | Supports more complex reasoning |

The grounding module will be evaluated by comparing the selected image or target region with the expected ground truth. If the project uses a simulator or robot, grounding can be connected to actual goal selection.

## 3.9 Navigation Decision Module

The navigation decision module converts the grounded target into a navigation output. Two decision styles are considered.

The first style follows the `LM-Nav` approach. The system selects a visual goal or landmark and passes it to a navigation model. This is suitable when the robot or simulator has a goal-conditioned navigation policy.

The second style follows the `VLMnav` approach. The current observation and instruction are given to a VLM, and the VLM selects the next action from a fixed action set. Example actions may include:

- move forward
- turn left
- turn right
- stop
- search

**Table 3.11: Navigation Decision Methods**

| Method | Input | Output | Reference |
|---|---|---|---|
| Landmark-to-goal selection | Extracted landmark and candidate images | Selected visual goal | `LM-Nav` |
| VLM action question answering | Instruction, current view, and action choices | Next action | `VLMnav` |
| Map-based goal selection | Instruction and semantic map | Goal coordinate or region | `VLMaps` |
| Scene-graph-based planning | Instruction and 3D scene graph | Room, object, or path target | `HOV-SG` |

For this project, the main implementation can begin with landmark-to-goal selection because it is closest to `LM-Nav`. The VLM action question-answering method can be used as an improvement or comparison.

## 3.10 Baseline and Proposed Improvements

The baseline method is the original `LM-Nav` style pipeline. In this baseline, the LLM extracts landmarks, CLIP grounds the landmarks in images, and the selected image goal is used for navigation.

The proposed project improves the baseline by focusing on prompt engineering. Instead of extracting only landmark names, the improved prompt attempts to extract a richer navigation plan containing landmarks, route order, spatial relations, and constraints.

**Table 3.12: Baseline and Improvement Methods**

| Method | Description | Purpose |
|---|---|---|
| Baseline LM-Nav prompt | Extracts ordered landmarks only | Establish baseline performance |
| Structured navigation prompt | Extracts landmarks, target, relations, and constraints | Improve output completeness |
| Relation-aware grounding prompt | Converts extracted relations into grounding descriptions | Improve visual target matching |
| VLMnav-style action prompt | Converts the navigation problem into multiple-choice action selection | Compare direct action reasoning |
| Optional map or scene memory | Uses map or scene representation for grounding | Future improvement inspired by `VLMaps` and `HOV-SG` |

The comparison between these methods will show whether structured prompt engineering improves the navigation pipeline compared with simple landmark extraction.

## 3.11 Implementation Procedure

The implementation is conducted in stages to reduce complexity and allow each module to be validated before full integration.

**Table 3.13: Implementation Procedure**

| Step | Activity | Verification | Expected Result |
|---|---|---|---|
| 1 | Prepare navigation instruction set | Manual inspection | Instructions cover simple and complex cases |
| 2 | Prepare candidate visual observations | Image review | Images contain relevant landmarks |
| 3 | Create baseline LM-Nav prompt | Prompt test | LLM returns landmark list |
| 4 | Create structured prompt | Schema validation | LLM returns valid structured output |
| 5 | Annotate expected landmarks and targets | Annotation review | Ground truth labels are available |
| 6 | Run landmark extraction experiments | Output comparison | Extraction scores are recorded |
| 7 | Run CLIP or VLM grounding experiments | Target comparison | Grounding scores are recorded |
| 8 | Run action or goal selection experiments | Scenario review | Navigation decision is generated |
| 9 | Compare baseline and improved prompts | Metric analysis | Best prompt design is identified |
| 10 | Analyze failure cases | Qualitative review | Limitations and improvements are documented |

This staged implementation follows the same logic as the university methodology reference, where each subsystem is built, verified, and then integrated into the final workflow.

## 3.12 Testing and Validation Plan

Testing is planned at three levels: module testing, integration testing, and scenario testing.

Module testing evaluates each component separately. The landmark extraction module is tested using text instructions. The grounding module is tested using candidate images and target labels. The navigation decision module is tested using instruction-image scenarios.

Integration testing evaluates the complete pipeline from instruction input to final goal or action output. Scenario testing evaluates the system on different instruction types, including easy, medium, and difficult cases.

**Table 3.14: Testing and Validation Matrix**

| Test Stage | Test Setup | Metric | Pass Criteria |
|---|---|---|---|
| Stage 1: Prompt format test | Input instructions only | Valid output rate | Most outputs follow the required schema |
| Stage 1: Landmark extraction test | Instructions with expected landmarks | Extraction accuracy | Correct target landmarks are identified |
| Stage 1: Spatial relation test | Instructions with relation labels | Relation accuracy | Relations such as near, beside, and after are extracted correctly |
| Stage 2: Grounding test | Text goals and candidate images | Top-1 or Top-k accuracy | Correct image or target is selected |
| Stage 2: Action selection test | Instruction and current view | Action correctness | Selected action matches expected direction |
| Stage 3: Full pipeline test | Instruction to final goal/action | Task success | Final output is relevant to the navigation instruction |
| Stage 3: Robustness test | Ambiguous or complex instructions | Failure analysis | Failure cases are identified and categorized |
| Stage 3: Latency test | Full pipeline execution | Response time | Output is produced within acceptable time |

## 3.13 Evaluation Metrics

The evaluation uses both quantitative and qualitative metrics. Quantitative metrics provide measurable performance values, while qualitative analysis explains why the system succeeds or fails.

**Table 3.15: Evaluation Metrics**

| Metric | Description |
|---|---|
| Landmark extraction accuracy | Percentage of instructions where the correct landmarks are extracted |
| Spatial relation accuracy | Percentage of relations correctly extracted from instructions |
| Structured output validity | Percentage of outputs that follow the required schema |
| Grounding accuracy | Percentage of cases where the correct image or target is selected |
| Action selection accuracy | Percentage of cases where the selected action matches the expected action |
| Task success rate | Percentage of full scenarios that produce a correct final goal or action |
| Invalid output rate | Percentage of outputs that are incomplete, malformed, or unusable |
| Average latency | Average time needed to produce a final output |
| Model call count | Number of LLM or VLM calls needed per instruction |

Qualitative analysis will be used to study common failure cases. Possible failure categories include missing landmark, wrong landmark order, incorrect spatial relation, weak visual grounding, ambiguous instruction, hallucinated output, or unsafe action suggestion.

## 3.14 Safety, Ethics, and Practical Considerations

Although this project is mainly a research prototype, safety must still be considered. If the system is connected to a simulator or physical robot, generated actions should not be executed directly without a safety layer. The robot should have obstacle avoidance, speed limits, emergency stop capability, and manual supervision.

Privacy is also important if camera images are collected from real environments. Images should avoid capturing identifiable people whenever possible, and any collected data should be stored only for research use.

The project should also acknowledge the limitations of LLM and VLM outputs. These models may hallucinate objects, misinterpret instructions, or produce inconsistent results. Therefore, the system should validate model outputs before using them for navigation.

## 3.15 Summary

This chapter described the research methodology for `Prompt Engineering for Mobile Robot Navigation`. The methodology is based on the `LM-Nav` pipeline, where an LLM extracts landmarks, a vision-language model grounds those landmarks, and a navigation model executes the selected goal. The project extends this baseline by focusing on structured prompt engineering, relation-aware extraction, visual grounding, and VLM-based action selection.

The proposed methodology includes instruction preparation, prompt template design, landmark and plan extraction, vision-language grounding, navigation decision making, testing, evaluation, and failure analysis. The chapter also links each method to the research objectives, defines the theoretical framework, identifies experimental parameters, and explains the validation procedure. This provides a structured foundation for implementing and analyzing the project in the following chapters.
