import cv2

# 读取图像
image = cv2.imread("../flower.png")
if image is None:
    print("无法加载图像，请检查文件路径。")
else:
    # 均值去噪
    blur_mean = cv2.blur(image, (5, 5))

    # 中值去噪
    blur_median = cv2.medianBlur(image, 5)

    # 高斯去噪
    blur_gaussian = cv2.GaussianBlur(image, (5, 5), 0)

    cv2.imwrite('Original Image.png', image)
    cv2.imwrite('Mean Blur.png', blur_mean)
    cv2.imwrite('Median Blur.png', blur_median)
    cv2.imwrite('Gaussian Blur.png', blur_gaussian)
    # 显示结果
    cv2.imshow('Original Image', image)
    cv2.imshow('Mean Blur', blur_mean)
    cv2.imshow('Median Blur', blur_median)
    cv2.imshow('Gaussian Blur', blur_gaussian)

    # 等待按键响应并关闭窗口
    cv2.waitKey(0)
    cv2.destroyAllWindows()
