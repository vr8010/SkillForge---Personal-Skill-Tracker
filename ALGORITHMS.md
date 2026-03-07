# 🧮 SkillForge Mastery Algorithms

## Overview

SkillForge implements 7 sophisticated mathematical algorithms for calculating skill mastery scores. Each algorithm models different aspects of learning and skill development, providing accurate and meaningful assessments.

## Algorithm Catalog

### 1. Linear Weighted Algorithm

**Purpose**: Simple, transparent scoring with diminishing returns

**Formula**:
```
Practice_Factor = min((Hours / Hour_Cap) × 100, 100)
Score = (Progress × 0.6) + (Practice_Factor × 0.4) × Weight_Factor
Final = min(Score, 100)
```

**Parameters**:
- `progress`: Skill progress percentage (0-100)
- `practice_hours`: Total hours practiced
- `weight_factor`: Multiplier for final score (default: 1.0)
- `hour_cap`: Hours needed for 100% practice factor (default: 100)

**Characteristics**:
- Linear relationship between inputs and output
- Diminishing returns on practice hours after cap
- Transparent and easy to understand
- Good baseline for comparison

**Best For**: General-purpose scoring, beginners

---

### 2. Exponential Growth Algorithm

**Purpose**: Rewards consistent practice with accelerating gains

**Formula**:
```
if Hours == 0:
    Score = Progress × 0.5 × Base_Multiplier
else:
    Growth_Factor = 1 + log(1 + Hours/10)
    Score = Progress × Growth_Factor × Base_Multiplier
Final = min(Score, 100)
```

**Parameters**:
- `progress`: Skill progress percentage (0-100)
- `practice_hours`: Total hours practiced
- `base_multiplier`: Scaling factor (default: 1.0)

**Characteristics**:
- Logarithmic growth curve
- Rewards consistent practice
- Accelerating returns early, then plateaus
- Penalizes zero practice heavily

**Best For**: Skills requiring consistent practice, technical skills

---

### 3. Sigmoid Curve Algorithm

**Purpose**: Models realistic S-curve learning patterns

**Formula**:
```
Combined_Input = (Progress + min(Hours, 100)) / 2
Score = 100 / (1 + e^(-steepness × (Combined_Input - 50)))
```

**Parameters**:
- `progress`: Skill progress percentage (0-100)
- `practice_hours`: Total hours practiced
- `steepness`: Curve steepness (default: 0.1)

**Characteristics**:
- S-shaped learning curve
- Slow start, rapid middle growth, plateau at end
- Realistic model of human learning
- Smooth transitions between levels

**Best For**: Soft skills, realistic learning modeling

---

### 4. Balanced Composite Algorithm

**Purpose**: Three-factor balanced approach

**Formula**:
```
Progress_Component = Progress × 0.4
Practice_Component = min((Hours / 100) × 100, 100) × 0.3
Additional_Component = Additional_Factor × Factor_Weight
Score = Progress_Component + Practice_Component + Additional_Component
Final = min(Score, 100)
```

**Parameters**:
- `progress`: Skill progress percentage (0-100)
- `practice_hours`: Total hours practiced
- `additional_factor`: Third factor (e.g., applications, difficulty)
- `factor_weight`: Weight for third factor (default: 0.3)

**Characteristics**:
- Balanced weighting across three factors
- Flexible third factor
- Equal consideration of multiple aspects
- Customizable weights

**Best For**: Skills with multiple measurable dimensions

---

### 5. Difficulty Adjusted Algorithm

**Purpose**: Scales scoring based on skill complexity

**Formula**:
```
Base_Score = (Progress × 0.5) + (min(Hours / 100, 1.0) × 100 × 0.3)
Difficulty_Bonus = (Difficulty / Max_Difficulty) × 0.2
Score = Base_Score × (1 + Difficulty_Bonus)
Final = min(Score, 100)
```

**Parameters**:
- `progress`: Skill progress percentage (0-100)
- `practice_hours`: Total hours practiced
- `difficulty`: Difficulty level (1-10)
- `max_difficulty`: Maximum difficulty (default: 10)

**Characteristics**:
- Rewards tackling difficult skills
- Bonus scales with difficulty
- Encourages challenging yourself
- Fair comparison across difficulty levels

**Best For**: Technical skills, complex subjects

---

### 6. Application Focused Algorithm

**Purpose**: Emphasizes real-world practical application

**Formula**:
```
Progress_Component = Progress × 0.35
Practice_Component = min((Hours / 50) × 100, 100) × 0.25
Application_Component = min((Applications / App_Cap) × 100, 100) × 0.4
Score = Progress_Component + Practice_Component + Application_Component
Final = min(Score, 100)
```

**Parameters**:
- `progress`: Skill progress percentage (0-100)
- `practice_hours`: Total hours practiced
- `applications`: Number of real-world applications
- `app_cap`: Applications needed for 100% (default: 20)

**Characteristics**:
- Heavily weights practical application (40%)
- Lower practice hour requirement (50h cap)
- Theory alone insufficient for high scores
- Encourages real-world usage

**Best For**: Soft skills, practical skills

---

### 7. Time Decay Algorithm

**Purpose**: Models skill degradation without practice

**Formula**:
```
Base_Score = (Progress × 0.6) + (min(Hours / 100, 1.0) × 100 × 0.4)
Decay_Factor = e^(-decay_rate × days_inactive)
Score = Base_Score × Decay_Factor
```

**Parameters**:
- `progress`: Skill progress percentage (0-100)
- `practice_hours`: Total hours practiced
- `days_since_update`: Days since last practice
- `decay_rate`: Decay speed (default: 0.01)

**Characteristics**:
- Exponential decay over time
- Encourages regular practice
- Realistic skill retention model
- Recoverable with renewed practice

**Best For**: Future feature, skill maintenance tracking

---

## Hybrid Models

### Technical Skills Hybrid

**Composition**: Difficulty-Adjusted (85%) + Exponential Growth (15%)

**Rationale**:
- Primary algorithm rewards complexity and effort
- Secondary algorithm encourages consistent practice
- Combines structural difficulty with growth mindset
- Balanced between achievement and dedication

**Formula**:
```python
primary = difficulty_adjusted(progress, hours, difficulty)
secondary = exponential_growth(progress, hours, multiplier=0.15)
final = (primary × 0.85) + (secondary × 0.15)
```

### Soft Skills Hybrid

**Composition**: Application-Focused (75%) + Sigmoid Curve (25%)

**Rationale**:
- Primary algorithm emphasizes practical application
- Secondary algorithm models realistic learning curves
- Combines action-oriented with natural learning patterns
- Encourages real-world practice over theory

**Formula**:
```python
primary = application_focused(progress, hours, applications)
secondary = sigmoid_curve(progress, hours, steepness=0.08)
final = (primary × 0.75) + (secondary × 0.25)
```

---

## Mastery Level Classification

Scores are mapped to descriptive levels:

| Score Range | Level | Badge | Description |
|-------------|-------|-------|-------------|
| 90-100 | Master | 🏆 | Complete mastery achieved |
| 75-89 | Expert | ⭐ | High proficiency demonstrated |
| 60-74 | Advanced | 💪 | Strong competency level |
| 40-59 | Intermediate | 📈 | Solid foundation established |
| 20-39 | Beginner | 🌱 | Learning in progress |
| 0-19 | Novice | 🔰 | Just starting out |

---

## Visual Representation

### Progress Bars

ASCII-based visualization of mastery scores:

```
[████████████████████] 100.0%  (Full mastery)
[███████████████░░░░░]  75.0%  (Expert level)
[██████████░░░░░░░░░░]  50.0%  (Intermediate)
[█████░░░░░░░░░░░░░░░]  25.0%  (Beginner)
[░░░░░░░░░░░░░░░░░░░░]   0.0%  (Not started)
```

**Implementation**:
```python
filled = int((score / 100) × width)
empty = width - filled
bar = "█" × filled + "░" × empty
```

---

## Algorithm Selection Guide

### When to Use Each Algorithm

| Algorithm | Use Case | Skill Type | Complexity |
|-----------|----------|------------|------------|
| Linear Weighted | General purpose, baseline | Any | Low |
| Exponential Growth | Consistent practice rewards | Technical | Medium |
| Sigmoid Curve | Realistic learning curves | Soft | Medium |
| Balanced Composite | Multi-dimensional skills | Any | Medium |
| Difficulty Adjusted | Complex technical skills | Technical | High |
| Application Focused | Practical soft skills | Soft | Medium |
| Time Decay | Maintenance tracking | Any | High |

### Comparison Matrix

| Algorithm | Progress Weight | Practice Weight | Other Factors | Growth Pattern |
|-----------|----------------|-----------------|---------------|----------------|
| Linear Weighted | 60% | 40% | None | Linear |
| Exponential Growth | Variable | Variable | None | Exponential |
| Sigmoid Curve | 50% | 50% | None | S-Curve |
| Balanced Composite | 40% | 30% | 30% | Linear |
| Difficulty Adjusted | 50% | 30% | 20% (Difficulty) | Linear + Bonus |
| Application Focused | 35% | 25% | 40% (Applications) | Linear |
| Time Decay | 60% | 40% | Decay Factor | Exponential Decay |

---

## Mathematical Properties

### Normalization

All algorithms normalize inputs to prevent overflow:
- Progress: Already 0-100
- Practice hours: Capped at algorithm-specific limits
- Additional factors: Normalized to 0-100 range

### Bounds

All algorithms guarantee:
- Minimum score: 0
- Maximum score: 100
- Monotonic increase with positive inputs
- Continuous functions (no jumps)

### Sensitivity Analysis

| Algorithm | Progress Sensitivity | Practice Sensitivity | Other Sensitivity |
|-----------|---------------------|---------------------|-------------------|
| Linear Weighted | High | Medium | N/A |
| Exponential Growth | High | High | N/A |
| Sigmoid Curve | Medium | Medium | N/A |
| Balanced Composite | Medium | Medium | Medium |
| Difficulty Adjusted | High | Medium | Medium |
| Application Focused | Medium | Low | High |
| Time Decay | High | Medium | High |

---

## Implementation Notes

### Strategy Pattern

Algorithms are implemented as static methods in `MasteryAlgorithm` class:
- No state required
- Pure functions
- Easy to test
- Composable

### Extensibility

Adding new algorithms:
1. Add static method to `MasteryAlgorithm` class
2. Follow signature: `(progress, hours, ...) -> float`
3. Ensure output range [0, 100]
4. Document formula and rationale

### Performance

All algorithms are O(1) time complexity:
- Simple arithmetic operations
- No loops or recursion
- Efficient for real-time calculation

---

## Future Enhancements

### Planned Algorithms

1. **Neural Network Model**: ML-based personalized scoring
2. **Comparative Ranking**: Score relative to peer group
3. **Goal-Oriented**: Score based on target achievement
4. **Adaptive Weighting**: Self-adjusting factor weights

### Advanced Features

1. **Algorithm Recommendation**: Suggest best algorithm per skill
2. **Custom Algorithms**: User-defined formulas
3. **A/B Testing**: Compare algorithm effectiveness
4. **Trend Analysis**: Historical algorithm performance

---

## References

### Mathematical Foundations

- Sigmoid Function: Logistic growth model
- Exponential Growth: Compound interest model
- Time Decay: Radioactive decay model
- Normalization: Min-max scaling

### Learning Science

- S-Curve: Diffusion of innovations theory
- Deliberate Practice: Ericsson's expertise research
- Spaced Repetition: Ebbinghaus forgetting curve
- Transfer Learning: Application-based mastery

---

**Version**: 1.2.0  
**Last Updated**: 2026-03-05  
**Author**: SkillForge Development Team
