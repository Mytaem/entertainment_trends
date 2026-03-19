# ==============================================================================
# BÁO CÁO PHÂN TÍCH DỮ LIỆU YOUTUBE TẠI VIỆT NAM (REPORT 3)
# ==============================================================================

# ------------------------------------------------------------------------------
# PHẦN 1: CÀI ĐẶT THƯ VIỆN & KẾT NỐI DATABASE
# ------------------------------------------------------------------------------
library(DBI)
library(RPostgreSQL)
library(dplyr)
library(ggplot2)
library(lubridate)
library(scales) # Dùng để phẩy hàng nghìn (1,000,000)

options(scipen = 999) # Tắt hiển thị số mũ khoa học (e+06)

# 1. Kết nối với cơ sở dữ liệu PostgreSQL
conn <- dbConnect(dbDriver("PostgreSQL"),
                  host = "localhost", 
                  port = 5432,
                  dbname = "ady_database", 
                  user = "mytam_vankhanh", 
                  password = "123")

# 2. Rút toàn bộ dữ liệu từ bảng youtube_final
df_youtube <- dbGetQuery(conn, "SELECT * FROM youtube_final")

# ------------------------------------------------------------------------------
# PHẦN 2: TIỀN XỬ LÝ DỮ LIỆU (DATA PREPROCESSING)
# ------------------------------------------------------------------------------
# Lọc dữ liệu riêng cho thị trường Việt Nam và chuyển đổi múi giờ
df_vn <- df_youtube %>%
  filter(country == "VN") %>%
  mutate(
    publish_time_utc = ymd_hms(publish_time),
    publish_time_vn = with_tz(publish_time_utc, tzone = "Asia/Ho_Chi_Minh")
  )

# ------------------------------------------------------------------------------
# PHẦN 3: TRỰC QUAN HÓA DỮ LIỆU (DATA VISUALIZATION)
# ------------------------------------------------------------------------------

# --- BIỂU ĐỒ 1: MỐI TƯƠNG QUAN TƯƠNG TÁC & LƯỢT XEM (SCATTER PLOT) ---
df_interaction <- df_vn %>%
  mutate(
    total_interaction = as.numeric(likes) + as.numeric(comments),
    views = as.numeric(views)
  ) %>%
  filter(total_interaction > 0, views > 0)

p1_scatter <- ggplot(df_interaction, aes(x = total_interaction, y = views)) +
  geom_point(color = "#0073C2", alpha = 0.5, size = 2) + 
  geom_smooth(method = "lm", color = "red", linetype = "dashed", size = 1.2) + 
  scale_x_log10(labels = scales::comma) + 
  scale_y_log10(labels = scales::comma) + 
  labs(
    title = "MỐI TƯƠNG QUAN GIỮA MỨC ĐỘ TƯƠNG TÁC VÀ LƯỢT XEM",
    subtitle = "Thuật toán YouTube: Lượng Like + Comment tỉ lệ thuận với lượng View",
    x = "Tổng lượng tương tác (Lượt Thích + Bình Luận)",
    y = "Tổng Lượt Xem (Views)"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", size = 14),
    plot.subtitle = element_text(size = 11, color = "gray40"),
    axis.title = element_text(face = "bold", size = 11),
    axis.text = element_text(face = "bold", size = 10),
    panel.grid.minor = element_blank()
  )
print(p1_scatter)

# --- BIỂU ĐỒ 2: TỶ LỆ TƯƠNG TÁC THEO THỂ LOẠI (BAR CHART) ---
df_er_category <- df_vn %>%
  filter(as.numeric(views) > 0) %>%
  mutate(engagement_rate = (as.numeric(likes) + as.numeric(comments)) / as.numeric(views) * 100) %>%
  group_by(category_name) %>%
  summarise(avg_er = mean(engagement_rate, na.rm = TRUE), total_videos = n()) %>%
  filter(total_videos > 5) %>% 
  arrange(desc(avg_er)) %>% 
  head(10)

p2_category <- ggplot(df_er_category, aes(x = reorder(category_name, avg_er), y = avg_er)) +
  geom_col(fill = "#0073C2", alpha = 0.85, width = 0.65) + 
  geom_text(aes(label = paste0(round(avg_er, 2), "%")), hjust = -0.15, size = 4, fontface = "bold", color = "#282828") + 
  coord_flip() + 
  scale_y_continuous(expand = expansion(mult = c(0, 0.2))) +
  labs(
    title = "THỂ LOẠI SỞ HỮU CỘNG ĐỒNG TƯƠNG TÁC TỐT NHẤT",
    subtitle = "Top 10 thể loại có Tỷ lệ tương tác (ER) cao nhất",
    x = "Thể loại Nội dung (Category)", 
    y = "Tỷ lệ tương tác trung bình (%)"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", size = 14),
    plot.subtitle = element_text(size = 11, color = "gray40"),
    axis.title = element_text(face = "bold", size = 11),
    axis.text = element_text(face = "bold", size = 10),
    panel.grid.minor = element_blank(),
    panel.grid.major.y = element_blank()
  )
print(p2_category)

# --- BIỂU ĐỒ 3: HIỆU SUẤT THEO NGÀY TRONG TUẦN (COLUMN CHART) ---
df_day_of_week <- df_vn %>%
  mutate(
    dow_num = wday(publish_time_vn, week_start = 1), 
    day_name = case_when(
      dow_num == 1 ~ "Thứ 2", dow_num == 2 ~ "Thứ 3", dow_num == 3 ~ "Thứ 4",
      dow_num == 4 ~ "Thứ 5", dow_num == 5 ~ "Thứ 6", dow_num == 6 ~ "Thứ 7", dow_num == 7 ~ "Chủ Nhật"
    ),
    day_name = factor(day_name, levels = c("Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"))
  ) %>%
  filter(!is.na(day_name)) %>% 
  group_by(day_name) %>%
  summarise(avg_views = mean(as.numeric(views), na.rm = TRUE) / 1000000)

p3_day <- ggplot(df_day_of_week, aes(x = day_name, y = avg_views)) +
  geom_col(fill = "#0073C2", alpha = 0.85, width = 0.55) +
  geom_text(aes(label = round(avg_views, 2)), vjust = -0.8, size = 4, fontface = "bold", color = "#282828") + 
  scale_y_continuous(expand = expansion(mult = c(0, 0.2))) + 
  labs(
    title = "HIỆU SUẤT LƯỢT XEM THEO NGÀY TRONG TUẦN",
    subtitle = "Trung bình lượt xem phân bổ từ Thứ 2 đến Chủ nhật",
    x = "Ngày xuất bản", 
    y = "Lượt xem trung bình (Triệu Views)"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", size = 14),
    plot.subtitle = element_text(size = 11, color = "gray40"),
    axis.title = element_text(face = "bold", size = 11),
    axis.text = element_text(face = "bold", size = 10),
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_blank()
  )
print(p3_day)

# --- CHUẨN BỊ DỮ LIỆU CHO BIỂU ĐỒ 4 & 5 (PHÂN TÍCH KHUNG GIỜ) ---
baseline_er <- df_vn %>%
  filter(as.numeric(views) > 0) %>%
  summarise(overall_er = mean((as.numeric(likes) + as.numeric(comments)) / as.numeric(views) * 100, na.rm = TRUE)) %>%
  pull(overall_er)

df_hourly_full <- df_vn %>%
  filter(as.numeric(views) > 0) %>%
  mutate(hour = hour(publish_time_vn)) %>%
  group_by(hour) %>%
  summarise(
    avg_views = mean(as.numeric(views), na.rm = TRUE) / 1000000,
    hourly_er = mean((as.numeric(likes) + as.numeric(comments)) / as.numeric(views) * 100, na.rm = TRUE),
    virality = round(hourly_er / baseline_er, 2) 
  )

# --- BIỂU ĐỒ 4: LƯỢT XEM THEO KHUNG GIỜ (LINE CHART) ---
p4_hour_views <- ggplot(df_hourly_full, aes(x = hour, y = avg_views)) +
  geom_line(color = "#0073C2", size = 1.2) + 
  geom_point(color = "#0073C2", size = 3) +
  geom_text(aes(label = round(avg_views, 2)), vjust = -1.2, size = 3.5, fontface = "bold", color = "#282828") +
  scale_x_continuous(breaks = 0:23, limits = c(0, 23)) + 
  scale_y_continuous(expand = expansion(mult = c(0.1, 0.25))) +
  labs(
    title = "PHÂN TÍCH HIỆU QUẢ KHUNG GIỜ VÀNG",
    subtitle = "Lượt xem trung bình theo giờ xuất bản (Múi giờ VN)",
    x = "Khung giờ trong ngày (00h - 23h)",
    y = "Lượt xem (Triệu views)"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", size = 14),
    plot.subtitle = element_text(size = 11, color = "gray40"),
    axis.title = element_text(face = "bold", size = 11),
    axis.text = element_text(face = "bold", size = 10),
    panel.grid.minor = element_blank()
  )
print(p4_hour_views)

# --- BIỂU ĐỒ 5: ĐIỂM VIRALITY THEO KHUNG GIỜ (LINE CHART) ---
p5_virality <- ggplot(df_hourly_full, aes(x = hour, y = virality)) +
  geom_line(color = "#0073C2", size = 1.2) +
  geom_point(color = "#0073C2", size = 3) +
  geom_text(aes(label = virality), vjust = -1.2, size = 3.5, fontface = "bold", color = "#282828") +
  scale_x_continuous(breaks = 0:23, limits = c(0, 23)) + 
  scale_y_continuous(expand = expansion(mult = c(0.1, 0.25))) +
  labs(
    title = "BIẾN ĐỘNG CHỈ SỐ VIRALITY THEO KHUNG GIỜ",
    subtitle = "Mức độ lan truyền và tương tác thực tế của video",
    x = "Khung giờ trong ngày (00h - 23h)",
    y = "Điểm Virality"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", size = 14),
    plot.subtitle = element_text(size = 11, color = "gray40"),
    axis.title = element_text(face = "bold", size = 11),
    axis.text = element_text(face = "bold", size = 10),
    panel.grid.minor = element_blank()
  )
print(p5_virality)

# ==============================================================================
# ĐÓNG KẾT NỐI (Rất quan trọng khi làm việc với Database)
# ==============================================================================
dbDisconnect(conn)