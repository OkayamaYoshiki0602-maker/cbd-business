# X Developer Portal Use Case Description (English Version)

## 📋 For X Developer Portal Form Submission

This file contains the English version of the use case description for the X Developer Portal form.

---

## Use Cases for X Data and API (English)

### 1. Project Overview

**Project Name:** CBD Information Site Management & Auto-Posting System

**Purpose:** To automate the management of "CBD WORLD" (https://cbd-no-hito.com/), an information website about CBD (Cannabidiol), and continuously provide valuable information to users through an automated system.

---

### 2. Specific Use Cases

#### 2.1 Automatic Posting of Site Articles

**Purpose:**
Automatically share newly published WordPress articles on X to increase traffic to the site.

**Implementation:**
- Detect new articles using WordPress RSS feed or Webhook
- Automatically generate tweet text (within 280 characters) from article title and summary
- Post to X with article URL
- Confirm content via LINE notification before posting (human verification)

**APIs Used:**
- `POST /2/tweets` - Post tweets
- `POST /1.1/media/upload` - Upload images (article thumbnails)

**Posting Frequency:**
- Only when new articles are published (typically 0-2 times per day)
- No spam behavior
- Comply with rate limits

**Content:**
- Article title and summary
- Article URL
- Relevant hashtags (#CBD #health #sleep, etc.)
- Site brand name ("CBD WORLD")

---

#### 2.2 Sharing CBD-Related News

**Purpose:**
Quickly share the latest CBD industry news and research results with users.

**Implementation:**
- Monitor RSS feeds from reliable CBD information sources (official sites of research institutions, medical information sites, etc.)
- When new news is detected, automatically generate tweets with summary and source URL
- Confirm content via LINE notification before posting (human verification)
- Ensure accuracy of medical/health content through expert verification when necessary

**APIs Used:**
- `POST /2/tweets` - Post tweets

**Posting Frequency:**
- Only when news is published (typically 0-3 times per day)
- Prioritize quality of information, no spam behavior

**Content:**
- News summary (within 280 characters)
- Source URL
- Relevant hashtags
- Site brand name

---

#### 2.3 Promotion of Diagnostic Tool

**Purpose:**
Promote the "CBD Personal Diagnostic Tool" on the site at appropriate times via X.

**Implementation:**
- Periodically post tweets introducing the diagnostic tool's features and characteristics
- Create guidance text based on user concerns (sleep, stress, concentration, etc.)
- Post with diagnostic tool URL

**APIs Used:**
- `POST /2/tweets` - Post tweets

**Posting Frequency:**
- 1-2 times per week (avoid excessive posting)
- Focus on user engagement

---

#### 2.4 User Engagement Enhancement

**Purpose:**
Maintain communication with X followers (currently about 1,000) and increase site repeaters.

**Implementation:**
- Utilize site access analytics data (Google Analytics 4) to understand popular articles and trends
- Select topics that users may be interested in
- Post human-created tweet text at appropriate times
- No automated replies or spam behavior

**APIs Used:**
- `POST /2/tweets` - Post tweets
- `GET /2/tweets/search/recent` - Search for replies and mentions (future implementation)

---

### 3. Data Usage

**Data Retrieved:**
- Tweet posting results (post ID, URL, etc.)
- Tweet engagement (likes, retweets, etc.) - future implementation
- User information (only own account information)

**Data Usage:**
- Recording posting history
- Engagement analysis (optimizing posting timing)
- Measuring traffic effect to the site

**Data Storage & Sharing:**
- Posting history is stored only in local environment
- No resale of data to third parties whatsoever
- Respect user privacy, no collection of personal information

---

### 4. Compliance with Automation Rules

**Compliance Items:**
- ✅ No spam behavior (avoid excessive posting)
- ✅ No automated replies or automated mentions
- ✅ Post content is confirmed by humans before posting
- ✅ Comply with X Terms of Service and Developer Agreement
- ✅ Comply with rate limits
- ✅ Respect user privacy

**Automation Scope:**
- Automate: article update detection, tweet text generation, posting scheduling
- **Human confirmation via LINE notification is required before posting execution**
- Do not post inappropriate content or content that may be judged as spam

---

### 5. Commercial Use

**Commercial Purpose:**
- Operating an affiliate site for CBD products
- Earn revenue from affiliate links on the site
- Purpose of tweets on X is to drive traffic to the site

**Revenue Model:**
- Commissions from affiliate links (on the site)
- No direct monetization using X API
- No resale of X data whatsoever

---

### 6. Technical Implementation

**Development Environment:**
- Python 3.9+
- tweepy library (X API v2)
- WordPress REST API (article update detection)
- LINE Messaging API (pre-posting confirmation)

**Operations:**
- Run on local environment or private server
- Code management on GitHub
- Regular maintenance and updates

**Security:**
- Manage API credentials with environment variables (.env file)
- Do not commit credentials to Git
- Regular security checks

---

### 7. Future Expansion Plans

**Future Features Under Consideration:**
- Reply to replies and mentions (not automated, reply after human confirmation)
- Optimization of posting timing (integrated analysis of GA4 data and X engagement data)
- A/B testing functionality (measuring effectiveness of tweet text)

**When Implementing These Features:**
- Consult with X Developer Support in advance
- Check for changes to Developer Agreement
- Update use case application as needed

---

### 8. Summary

**Project Value:**
- Provide accurate information about CBD
- Contribute to improvement of user health and lifestyle
- Contribute to healthy community building on X platform

**Purpose of X API Usage:**
- Operational efficiency (automation)
- Continuous information provision to users
- Increase traffic to the site

**Compliance:**
- Comply with X Developer Agreement & Policy
- No spam behavior
- Respect user privacy
- No data resale

---

以上が、X APIの使用例です。ご質問がございましたら、お気軽にお問い合わせください。
