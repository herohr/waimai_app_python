from uuid import uuid1
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random


def rnd_char():
    """
    随机一个字母或者数字
    :return:
    """
    # 随机一个字母或者数字
    i = random.randint(1, 3)
    if i == 1:
        # 随机个数字的十进制ASCII码
        an = random.randint(97, 122)
    elif i == 2:
        # 随机个小写字母的十进制ASCII码
        an = random.randint(65, 90)
    else:
        # 随机个大写字母的十进制ASCII码
        an = random.randint(48, 57)
    # 根据Ascii码转成字符，return回去
    return chr(an)


# 　干扰
def rnd_dis():
    """
    随机一个干扰字
    :return:
    """
    d = ['^', '-', '~', '_', '.']
    i = random.randint(0, len(d) - 1)
    return d[i]


# 两个随机颜色都规定不同的区域，防止干扰字符和验证码字符颜色一样
# 随机颜色1:
def rnd_color():
    """
    随机颜色，规定一定范围
    :return:
    """
    return random.randint(64, 255), random.randint(64, 255), random.randint(64, 255)


# 随机颜色2:
def rnd_color2():
    '''
      随机颜色，规定一定范围
      :return:
      '''
    return random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)


def create_code():
    # 240 x 60:
    width = 60 * 4
    height = 60
    image = Image.new('RGB', (width, height), (192, 192, 192))
    # 创建Font对象:
    font = ImageFont.truetype('./font/Arial.ttf', 36)

    # 创建Draw对象:
    draw = ImageDraw.Draw(image)

    # 填充每个像素:
    for x in range(0, width, 20):
        for y in range(0, height, 10):
            draw.point((x, y), fill=rnd_color())

    # 填充字符
    _str = ""
    # 填入4个随机的数字或字母作为验证码
    for t in range(4):
        c = rnd_char()
        _str = "{}{}".format(_str, c)

        # 随机距离图片上边高度，但至少距离30像素
        h = random.randint(1, height - 30)
        # 宽度的化，每个字符占图片宽度1／4,在加上10个像素空隙
        w = width / 4 * t + 10
        draw.text((w, h), c, font=font, fill=rnd_color2())

    # 实际项目中，会将验证码 保存在数据库，并加上时间字段
    print("保存验证码 {} 到数据库".format(_str))

    # 给图片加上字符干扰，密集度由 w, h控制
    for j in range(0, width, 30):
        dis = rnd_dis()
        w = t * 15 + j

        # 随机距离图片上边高度，但至少距离30像素
        h = random.randint(1, height - 30)
        draw.text((w, h), dis, font=font, fill=rnd_color())

    # 模糊:

    image.filter(ImageFilter.BLUR)

    # uuid1 生成唯一的字符串作为验证码图片名称
    code = _str
    code_name = '{}.jpg'.format(uuid1())
    save_dir = './{}'.format(code_name)
    print(image.tobytes())

    print("已保存图片: {}".format(save_dir))


if __name__ == "__main__":
    create_code()
