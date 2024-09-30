# Memes as Cryptographic Schemes: Theory and Generation with Language Models

**Abstract**

This paper introduces a mathematical framework modeling internet memes as cryptographic schemes. By drawing parallels between meme dissemination and cryptographic principles, we formalize meme creation and interpretation processes. Additionally, we present a technique for generating such memes using Language Models (LLMs), automating key generation and template selection to encode messages effectively.

---

## 1. Introduction

Memes serve as modern units of cultural transmission, often embedding nuanced meanings accessible only to those with specific contextual knowledge. This selective communication mirrors cryptographic systems where information is concealed from unintended recipients. This paper formalizes memes within a cryptographic framework and explores automated generation techniques using LLMs.

---

## 2. Mathematical Framework

### 2.1. Key Components
Start of Selection

- **Message Space (M)**: Set of all possible messages a meme can convey.
- **Key Space (K)**: Shared knowledge or context required to interpret a meme.
- **Ciphertext Space (C)**: Set of all possible memes encoding messages.
- **Encryption Function (E)**: E: M × K → C
- **Decryption Function (D)**: D: C × K → M

### 2.2. Properties

- **Correctness**: D(E(m, k), k) = m for all m in M, k in K.
- **Security**: Depends on the secrecy and complexity of k. Widely known keys reduce security.
- **Confidentiality**: Achieved through the obscurity of k, akin to steganography.

End of Selection
```

---

## 3. Meme Generation Technique with LLMs

### 3.1. Overview

Utilizing LLMs to automate meme creation involves generating a key and selecting an appropriate template based on the input message. This process ensures that the meme encodes the desired message securely within the chosen context.

### 3.2. Steps
# Start of Selection

1. **Input Message (m)**: User provides the underlying idea or joke.
2. **Key Generation (k)**:
   - **LLM Analysis**: Identifies relevant contexts or shared knowledge related to m.
   - **Selection**: Chooses a key with adequate specificity and entropy.
3. **Template Selection**:
   - **LLM Recommendation**: Suggests meme templates aligning with m and k.
   - **Database Query**: Selects from a repository of templates tagged with relevant metadata.
4. **Content Generation**:
   - **Caption Creation**: LLM generates text that embeds m within k's context.
   - **Visual Adjustment**: Modifies the template to incorporate key elements.
5. **Meme Assembly**:
   - Combines selected template with generated captions and visuals.
6. **Validation**:
   - Ensures the meme conveys m to those with k while remaining ambiguous otherwise.
7. **Distribution**:
   - Shares the meme within the intended audience, maintaining key secrecy.

### 3.3. Example Workflow

**Message**: "Final exams are overwhelming this semester."

1. **Key (k)**: Shared student experiences with exams.

# End of Selection
```
2. **Template**: "This Is Fine" dog meme.
3. **Caption**:
   - **Top**: Original image of the dog in a burning room.
   - **Bottom**: "Final exams are fine" with added elements like textbooks.
4. **Assembly**: Overlay textbooks and modify speech bubble.
5. **Validation**: Reviewed by peers for clarity and secrecy.
6. **Distribution**: Posted in student groups before exams.

---

## 4. Conclusion

Modeling memes as cryptographic schemes offers a structured understanding of their role in selective communication. By leveraging LLMs for automated meme generation, creators can efficiently encode messages within culturally relevant contexts, enhancing both creativity and security in digital communication.

---

**References**

- Dawkins, R. (1976). *The Selfish Gene*. Oxford University Press.
- Shannon, C. E. (1949). Communication Theory of Secrecy Systems. *Bell System Technical Journal*, 28(4), 656–715.
- Stallings, W. (2017). *Cryptography and Network Security: Principles and Practice*. Pearson.