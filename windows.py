# Представляю мини операционную систему Windows Py
# Это первый релиз
# Еще необходимо написать документацию по разработке ПО для этой оси  :)
# В ближайшее время будет разработана.... конечно игра, какая-нибудь.
# Допиливать ее можно вечно... Будут вопросы - пишите.
# Фокус окна активирутся при клике в область хеадера (названия окна)
# После выбора цвета, снова выбирайте инструмент... потом допилю.
# Производительность на слабых ПК и телефонах не очень, скоро выйдет обновление
# с возможностью отключения прорисовки окна, если оно не в фокусе
# А вообще - пошел я учить ООП...
# P.S. Забыл в калькуляторе реализовать ввод отрицательных чисел. Исправим...


import canvas
import math
import datetime as dt

init = False  # флаг инициализации панели управления Paint
init_task = False # флаг инициализации панели задач
init_menu_icon = False
but = []  # массив параметров кнопок управления Paint-ом
but_ = [] # второй ряд кнопок Paint-а пришлось сделать отдельно
buff = [False, 0, 0] # Состояние мыши - передача параметров
stack = []
line_temp = []
rect_temp = []
circle_temp = []
fill_on = False

message_listering = [] # буфер сообщений между функциями, типа сообщение - слушатель, ввел уже на последних стадиях разработки.

color = [
    ['Red',     'Yellow',  'Green',      'Blue'],
    ['Magenta', 'Orange', 'Lime',       'Cyan'],
    ['Pink',    'Coral',  'LightGreen', 'LightBlue'],
    ['Indigo',  'Khaki',  'White',  'Black']
    ]
color_action = color[0][2] # Цвет для рисования по умолчанию
data_color = []  # Список координат и цветов окна Color, расчитывается в функции paint_color_window

theme = {               # темы для отрисовки окон и кнопок
    'windows_default':
    [
        'DarkGray',   # border окна
        'White',      # Фон окна
        'White',      # Цвет текста caption
        'DodgerBlue'  # Цвет шапки
    ]
}
theme_active = 'windows_default'  # активная тема по умолчанию

# список списков параметров созданных объектов
data_property = [
    ['taskbar', True, 30], # Панель задач - Имя, Вкл/Выкл, высота
    ['button', True, 10, 10, 80, 25, 'Start', False],  # Имя, вкл/выкл, x,y,width,height,caption, состояние кнопки (нажата или нет)
    ['window', False, 45, 40, 250, 250, 'Paint', False],  # Имя компонента, вкл/выкл, x, y, width, height, текст в header, фокус окна
    ['window', False, 55, 55, 250, 250, 'Calc', False],
    ['window', False, 60, 70, 240, 240, 'Color', False],
    ['start_menu', False, 0, 220, 100, 100, '', False] # Имя, Вкл/Выкл, x, y, width, height, focus
]

# Параметры иконок в меню "Start" - Имя, x, y, width, height, расчитывается в функции start_menu
menu_icon = [
    ['Paint', 0, 0, 0, 0],
    ['Calculator', 0, 0, 0, 0]
    ]

paint_obj = []  # список нарисованых объектов с параметрами, заполняется по ходу рисования в Paint-е



# Функция отрисовки окна, target нужен для определения - кто вызвал эту фкнкцию?

def window(x, y, width, height, caption, focus, target):
    global data_property 
    global buff
    global stack
    global message_listering
    border_col, background_content, text_col, header_col = theme[theme_active]
    border = 3
    height_caption = 20
    margin_text = 5
    canvas.fill_style('Black')
    canvas.fill_rect(x+1, y+1, width, height) # Тень окна
    canvas.fill_style(border_col)
    canvas.fill_rect(x, y, width, height) # Основное окно
    if focus:    
        canvas.fill_style(header_col)
    else:
        canvas.fill_style('Grey')
    canvas.fill_rect(x+border, y+border, width-border*2, height_caption)  # Окно шапки
    canvas.fill_style('Black')
    canvas.fill_text(caption, x+border+margin_text+1, y+border+15+1, 'Tahoma', 14, 'left')  # тень текста шапки
    canvas.fill_style(text_col)
    canvas.fill_text(caption, x+border+margin_text, y+border+15, 'Tahoma', 14, 'left')  # текст шапки
    canvas.fill_style(background_content)
    canvas.fill_rect(x+border, y+border*2+height_caption, width-border*2, height-border*3-height_caption)  # фон окна, контента
    
    x_but_close = x+width-margin_text-14+1
    y_but_close = y + 6
    canvas.fill_style('Black')
    canvas.fill_rect(x_but_close+1, y_but_close+1, 14, 14)
    canvas.fill_style('DarkGray')
    canvas.fill_rect(x_but_close, y_but_close, 14, 14)
    canvas.set_color('Black')
    canvas.line_width(2)
    canvas.radius_line(x_but_close+2, y_but_close+2, 135, 13)
    canvas.radius_line(x_but_close+2+9, y_but_close+2, 225, 13)
    
    # Реализацию вызовов нужных функций можно переделать с использованием передачи параметра-функции, возможно доработаю в следующих версиях
    
    if data_property[target][6] == 'Paint':
        paint(x+border, y+border*2+height_caption, width-border*2, height-border*3-height_caption, focus)
    if data_property[target][6] == 'Color':
        paint_color_window(x+border, y+border*2+height_caption, width-border*2, height-border*3-height_caption, focus)
    if data_property[target][6] == 'Calc':
        calc(x+border, y+border*2+height_caption, width-border*2, height-border*3-height_caption, focus)
    
    # Обработчик закрытия окна
    click, x_click, y_click = buff 
    if click:
        if x_but_close+14 > x_click > x_but_close and y_but_close+14 > y_click > y_but_close:
            message_listering.append(['window', caption, 'close'])
            buff[0] = False
        
    if click and not focus:
        if x < x_click < x + width and y < y_click < y + height_caption:
            message_listering.append(['window', caption, 'enable_focus'])
            buff[0] = False
        
# Функция отрисовки кнопки    
def button(x, y, width=80, height=25, caption='OK', press=False):
    if not press:
        # рисование тени
        canvas.fill_style('Black')
        canvas.fill_rect(x+1, y+1, width, height)
    canvas.fill_style(theme[theme_active][0])
    canvas.fill_rect(x, y, width, height)
    canvas.fill_style('Black')
    canvas.fill_text(caption, x + width/2, y+height*0.7, font='Tahoma', size=12, align='center')
    

# Функция создания объектов из списка data_property
def create_object():
    canvas.fill_style('LightskyBlue')
    canvas.fill_rect(0,0,349,349)
    canvas.fill_style('CornflowerBlue')
    canvas.fill_text('Windows Py', 175, 50, font='Tahoma', size=42, align='center')
    global stack
    el_focus = -1
    if data_property:
        for index, el in enumerate(data_property, 0):
            if el[0] == 'window' and el[7]:
                el_focus = index
            if el[0] == 'button' and el[1]:
                obj, show, x, y, width, height, caption, press = el
                button(x, y, width, height, caption, press)
            elif el[0] == 'window' and el[1]:
                obj, show, x, y, width, height, caption, focus = el
                window(x, y, width, height, caption, focus, index)
            elif el[0] == 'taskbar' and el[1]:
                obj, show, height = el
                taskbar(height)
            elif el[0] == 'start_menu' and el[1]:
                obj, show, x, y, width, height, non, focus = el
                start_menu(x, y, width, height, focus)
        if el_focus >= 0 and data_property[el_focus][1]:
            obj, show, x, y, width, height, caption, focus = data_property[el_focus]
            window(x, y, width, height, caption, focus, el_focus)
        

# Реализация paint-а
def paint(x, y, width, height, focus):
    global init 
    global data_property 
    global buff  # Буфер (список) для передачи состояния мыши и координат
    global but   # Список кнопок панели управления
    global but_
    global fill_on
    canvas.fill_style(theme[theme_active][0])
    height_panel = 55
    canvas.fill_rect(x, y, width, height_panel)
    canvas.fill_style('Black')
    canvas.fill_text('Панель инструментов', x+width/2, y+height/12/2, 'Tahoma', 12, 'center')
    if not init:  # инициализация, выполняется один раз.   
        x_but = x
        y_but = y + height/6 - height/10
        x_but_ = x
        y_but_ = y_but + height/12-1 + 2
        count_button_ = 3
        count_button = 5
        button_text = ['Point', 'Line', 'Rect', 'Circle', 'Color']
        button_text_ = ['New', 'Fill OFF', 'Undo']
        for i in range(5):
            but.append([x_but+i*width/count_button, y_but, width/count_button, height/12-1, button_text[i], False])
            button(but[i][0], but[i][1], but[i][2], but[i][3], but[i][4], but[i][5])
            if i < count_button_:
                but_.append([x_but_+i*width/count_button_, y_but_, width/count_button_, height/12-1, button_text_[i], False])
                button(but_[i][0], but_[i][1], but_[i][2], but_[i][3], but_[i][4], but_[i][5])
        init = True
    else:
        # Если инициализация была выполнена, выполняется код ниже
        for index, el in enumerate(but, 0):
            x_butt, y_butt, width_butt, height_butt, caption_butt, press = el
            click, x_click, y_click = buff 
            # Здесь идет расчет, чтобы была нажата только одна из кнопок верхнего ряда
            if click and x_butt + width_butt > x_click > x_butt and y_butt + height_butt > y_click > y_butt and focus:
                but[index][5] = True
                buff[0] = False
                for j in range(5):
                    if j != index:
                        but[j][5] = False
        
    click, x_click, y_click = buff
    for i in range(5):
        button(but[i][0], but[i][1], but[i][2], but[i][3], but[i][4], but[i][5])
        if i < len(but_):
            x_but, y_but, width_but, height_but, caption_but, press = but_[i]
            button(x_but, y_but, width_but, height_but, caption_but, press)
            if click:
                if x_but < x_click < x_but+width_but and y_but < y_click < y_but+height_but and focus:
                    if caption_but == 'New':
                        paint_obj.clear()
                    elif caption_but == 'Undo':
                        if paint_obj:
                            paint_obj.pop()
                    elif caption_but == 'Fill OFF':
                        but_[i][4] = 'Fill ON'
                        fill_on = True
                    elif caption_but == 'Fill ON':
                        but_[i][4] = 'Fill OFF'
                        fill_on = False
                    buff[0] = False
    
    paint_canvas(x, y + height_panel, width, height - height_panel, focus)
    paint_draw()
    
def paint_canvas(x_canvas, y_canvas, width_can, height_can, focus):
    global buff
    global but
    global paint_obj
    global line_temp
    global color_action
    global fill_on
    global data_property
    paint_color()
    click, x_click, y_click = buff
    if focus:
        for el in but:
            if el[5] and click:
                if x_canvas < x_click < x_canvas + width_can and y_canvas < y_click < y_canvas + height_can:
                    if el[4] == 'Point':
                        paint_obj.append(['point', x_click, y_click, color_action])
                    if el[4] == 'Line':
                        if len(line_temp) == 0:
                            line_temp.append(x_click)
                            line_temp.append(y_click)
                        else:
                            paint_obj.append(['line', x_click, y_click, line_temp[0], line_temp[1], color_action])
                            line_temp.clear()
                    if el[4] == 'Rect':
                        if len(rect_temp) == 0:
                            rect_temp.append(x_click)
                            rect_temp.append(y_click)
                        else:
                            paint_obj.append(['rect', rect_temp[0], rect_temp[1], x_click-rect_temp[0], y_click-rect_temp[1], color_action, fill_on])
                            rect_temp.clear()
                    if el[4] == 'Circle':
                        if len(circle_temp) == 0:
                            circle_temp.append(x_click)
                            circle_temp.append(y_click)
                        else:
                            R = pow(((x_click-circle_temp[0])**2 + (y_click-circle_temp[1])**2), 0.5)
                            if circle_temp[0] + R > x_canvas + width_can:
                                R = abs(x_canvas + width_can - circle_temp[0])
                            if circle_temp[0] - R < x_canvas:
                                R = abs(circle_temp[0] - x_canvas)
                            if circle_temp[1] + R > y_canvas + height_can:
                                R = abs(y_canvas + height_can - circle_temp[1])
                            if circle_temp[1] - R < y_canvas:
                                R = abs(circle_temp[1] - y_canvas)
                            paint_obj.append(['circle', circle_temp[0], circle_temp[1], R, color_action, fill_on])
                            circle_temp.clear()
                    buff[0] = False
                            
                else:
                    paint_cancel()
# функция отмены не завершенных рисованных фигур, если нажатие было не по холсту
def paint_cancel():
    line_temp.clear()
    rect_temp.clear()
    circle_temp.clear()
                
def paint_draw():
    global paint_obj
    for el in paint_obj:
        if el[0] == 'point':
            canvas.fill_style(el[3])
            canvas.fill_circle(el[1], el[2], 2)
        if el[0] == 'line':
            canvas.set_color(el[5])
            canvas.move_to(el[1], el[2])
            canvas.line_to(el[3], el[4])
        if el[0] == 'rect':
            if el[6]:
                canvas.fill_style(el[5])
                canvas.fill_rect(el[1], el[2], el[3], el[4])
            else:
                canvas.set_color(el[5])
                canvas.stroke_rect(el[1], el[2], el[3], el[4])
        if el[0] == 'circle':
            if el[5]:
                canvas.fill_style(el[4])
                canvas.fill_circle(el[1], el[2], el[3])
            else:
                canvas.set_color(el[4])
                canvas.circle(el[1], el[2], el[3])
            
# обработчик нажатия кнопки Color
def paint_color():
    global data_property
    global but
    global message_listering
    if but[4][5]:
        message_listering.append(['window', 'Color', 'enable_focus'])
        message_listering.append(['window', 'Paint', 'no_focus'])
        but[4][5] = False
        
        # В первой версии почти в каждой функции были подобные проверки for-ом,
        # после введения системы сообщений message_listering я ускорил работу программы,
        # кроме того, стало легче управлять элементами через глобальный массив (список)
        #for index, el in enumerate(data_property, 0):
        #    if el[0] == 'window' and el[6] == 'Color':
        #        el[1] = True
        #        el[7] = True
        #        but[4][5] = False
        #    if el[0] == 'window' and el[6] == 'Paint':
        #        el[7] = False
        #        stack.append(index)
            
            
# Прорисовка контента окна Color и выбор цвета                
def paint_color_window(x_win, y_win, width, height, focus):
    global data_color
    global buff
    global color_action
    global message_listering
    click, x_click, y_click = buff 
    for i in range(len(color)):
        for j in range(len(color[0])):
            width_rect = width/len(color[0])
            height_rect = height/len(color)
            canvas.fill_style(color[i][j])
            canvas.fill_rect(x_win + width_rect*j, y_win + height_rect*i, width_rect, height_rect)
            data_color.append([x_win + width_rect*j, y_win + height_rect*i, width_rect, height_rect, color[i][j]])

    if click and focus:
        for el in data_color:
            x, y, wid, hei, col = el
            if x < x_click < x + wid and y < y_click < y + hei:
                color_action = col
                print(col)
                buff[0] = False
                message_listering.append(['window', 'Color', 'close'])
                message_listering.append(['window', 'Paint', 'enable_focus'])
                break
            
# Панель задач с часами
def taskbar(height):
    global buff
    global init_task
    global message_listering
    click, x_click, y_click = buff
    border_col, background_content, text_col, header_col = theme[theme_active]
    x, y, width = 0, 349 - height, 349 
    
    for el in data_property:
        if el[0] == 'button' and el[6] == 'Start':
            if not init_task:
                el[2], el[3], el[4], el[5] = x + 2, y + 2, 50, height - 4
                init_task = True
            else:
                if click:
                    if el[2] < x_click < el[2] + el[4] and el[3] < y_click < el[3] + el[5]:
                        message_listering.append(['start_menu', '', 'enable_focus'])
                        buff[0] = False
                        
            
    canvas.fill_style('SlateGray')
    canvas.fill_rect(x, y-2, width, height)
    canvas.fill_style(border_col)
    canvas.fill_rect(x, y, width, height)
    
    time_ = dt.datetime.now()
    time_str = time_.strftime("%H:%M")
    day_str = time_.strftime("%d")
    canvas.fill_style('Black')
    canvas.fill_text(time_str, x + 320, y + 20, 'Tahoma', 14, 'center')
    
    
    
# Меню пуск    
def start_menu(x, y, width, height, focus):
    global buff
    global menu_icon
    global init_menu_icon
    global message_listering
    border_col, background_content, text_col, header_col = theme[theme_active]
    for el in data_property:
        if el[0] == 'start_menu' and el[1]:
            pass
    canvas.fill_style('Black')
    canvas.fill_rect(x, y, width+1, height)
    canvas.fill_style(border_col)
    canvas.fill_rect(x, y, width, height)
    if not init_menu_icon:
        for index, el in enumerate(menu_icon, 0):
            el[1], el[2], el[3], el[4] = x + 2, y + 2 + 27*index, width - 4, 25
        init_menu_icon = True
    else:
        click, x_click, y_click = buff
        for index, el in enumerate(menu_icon, 0):
            text, x_icon, y_icon, width_icon, height_icon = el
            canvas.fill_style('Silver')
            canvas.fill_rect(x_icon, y_icon, width_icon, height_icon)
            canvas.fill_style('Black')
            canvas.fill_text(text, x + 2 + width_icon/2, y_icon + 17, 'Tahoma', 14, 'center')
            if click:
                if x_icon < x_click < x_icon + width_icon and y_icon < y_click < y_icon + height_icon:
                    if text == 'Paint':
                        message_listering.append(['window', 'Paint', 'enable_focus'])
                        message_listering.append(['start_menu', '', 'close'])
                    if text == 'Calculator':
                        message_listering.append(['window', 'Calc', 'enable_focus'])
                        message_listering.append(['start_menu', '', 'close'])
                    if text == 'XXX_Por':
                        message_listering.append(['XXX', 'XXX', 'enable_focus'])
                        message_listering.append(['start_menu', '', 'close'])
                else:
                    message_listering.append(['start_menu', '', 'close'])
                        
# Так называемый слушатель, обрабатывает сообщения.                         
def listering():
    global data_property
    global message_listering
    tmp_index = -1
    if message_listering:
        for el in message_listering:
            for index, el_dat in enumerate(data_property, 0):
                if el[0] == el_dat[0] and el[1] == el_dat[6]:
                    if el[2] == 'close':
                        el_dat[1] = False
                        el_dat[7] = False
                    if el[2] == 'enable_focus':
                        el_dat[1] = True
                        el_dat[7] = True
                        tmp_index = index
                    if el[2] == 'no_focus':
                        el_dat[7] = False
                    if el[2] == 'focus':
                        el_dat[7] = True
                    message_listering.remove(el)
    if tmp_index >= 0:
        for ind, el in enumerate(data_property, 0):
            if el[0] == 'window' and ind != tmp_index:
                el[7] = False

# -----------------Калькулятор --------------------------
# С калькулятором бился долго, реализаций возможно делать очень много
# Доробатывать можно вечно...

# Массив кнопок с координатами, расчитывается в основной функции calc
calc_butt = [
    [['C', 0, 0], ['MR', 0, 0], ['M+', 0, 0], ['MS', 0, 0]],
    [['7', 0, 0],  ['8', 0, 0],  ['9', 0, 0],  ['/', 0, 0]],
    [['4', 0, 0],  ['5', 0, 0],  ['6', 0, 0],  ['*', 0, 0]],
    [['1', 0, 0],  ['2', 0, 0],  ['3', 0, 0],  ['-', 0, 0]],
    [['0', 0, 0],  ['.', 0, 0],  ['=', 0, 0],  ['+', 0, 0]]
    ]
init_calc = False
lcd_value = '0' # Переменная напрямую связана с отображением на LCD калькулятора

def calc(x, y, width, height, focus):
    global calc_butt
    global init_calc
    global buff
    global lcd_value
    global memory
    border_col, background_content, text_col, header_col = theme[theme_active]
    canvas.set_color(border_col)
    canvas.stroke_rect(x + 5, y + 5, width - 10, 30)
    canvas.fill_style('Black')
    canvas.fill_text(lcd_value, x + width - 10, y + 5 + 30 - 7, 'Tahoma', 22, 'right')
    if memory[0] != 0:
        canvas.fill_style('Black')
        canvas.fill_text('M', x + 8, y + 18, 'Tahoma', 14, 'left')
    x_but, y_but, width_but, height_but = x + 5, y + 40, (width - 10)/len(calc_butt[0]) - 4 , (height - 45)/len(calc_butt) - 4
    border = 5
    click, x_click, y_click = buff
    if not init_calc:
        for i in range(len(calc_butt)):
            for j in range(len(calc_butt[0])):
                x_b = x_but + (width_but+border)*j
                y_b = y_but + (height_but+border)*i
                button(x_b, y_b, width_but, height_but, calc_butt[i][j][0], False)
                calc_butt[i][j][1] = x_b
                calc_butt[i][j][2] = y_b
                init_calc = True
    else:
        for i in range(len(calc_butt)):
            for j in range(len(calc_butt[0])):
                cap, x_but, y_but = calc_butt[i][j]
                button(x_but, y_but, width_but, height_but, cap, False)
                if click and focus:
                    if x_but < x_click < x_but + width_but and y_but < y_click < y_but + height_but:
                        calc_handler(cap)
                        buff[0] = False
                        
# Список параметров для алгоритма работы калькулятора
# Первое число, Второе число, первое Float или Int, второе Float или Int, Состояние калькулятора, Сивол операции
calc_data = ['0', '0', False, False, 0, '']
# Память калькулятора - значение, Float или Int
memory = [0, False]

def calc_reset_full():
    global lcd_value
    global calc_data
    global memory
    calc_data = ['0', '0', False, False, 0, '']
    lcd_value = '0'
    
def calc_reset():
    global lcd_value
    global calc_data
    calc_data = ['0', '0', False, False, 0, '']

# Основной алгоритм работы калькулятора
# С распаковками и упаковками данных нужно быть предельно внимательным:
# Запокавали данные и у вас уже не список а кортеж, его нельзя изменить поэлементно, только целиком.
# или после запаковки использовать list4
# Да и с внутреннеми распакованными переменными нужно аккуратнее, из за этого долго бился с 
# отладкой работы калькулятора
def calc_handler(sim):
    global lcd_value
    global memory
    global calc_data
    one, two, num_one_float, num_two_float, mode, oper = calc_data
    if sim == 'C':
        calc_reset_full()
    elif sim == 'MR':
        memory[0] = 0
        memory[1] = False
    elif sim == 'M+':
        if lcd_value != '0':
            if mode == 0:
                if num_one_float:
                    memory[0] += float(lcd_value)
                else:
                    memory[0] += int(lcd_value)
                memory[1] = num_one_float
            elif mode == 1:
                if num_two_float:
                    memory[0] += float(lcd_value)
                else:
                    memory[0] += int(lcd_value)
                memory[1] = num_two_float
        calc_reset()
    elif sim == 'MS':
        lcd_value = str(memory[0])
        if mode == 0:
            one = memory[0]
            num_one_float = memory[1]
        elif mode == 1:
            two = memory[0]
            num_two_float = memory[1]
        calc_data = one, two, num_one_float, num_two_float, mode, oper
    else:
        if mode == 0:
            if sim.isdigit():
                if one == '0':
                    one = sim
                else:
                    if len(one) < 12:
                        one += sim
            elif sim == '.' and not num_one_float:
                if len(one) < 12:
                    num_one_float = True
                    one += '.'
            elif sim in ('/', '*', '-', '+'):
                oper = sim
                mode = 1
                calc_data = one, two, num_one_float, num_two_float, mode, oper                    
                return
            lcd_value = one
            calc_data = one, two, num_one_float, num_two_float, mode, oper
        if mode == 1:
            if sim.isdigit():
                if two == '0':
                    two = sim
                else:
                    if len(two) < 12:
                        two += sim
            elif sim == '.' and not num_two_float:
                if len(two) < 12:
                    num_two_float = True
                    two += '.'
            lcd_value = two
            if sim == '=':
                mode = 2
                lcd_value = two
            calc_data = one, two, num_one_float, num_two_float, mode, oper
        if mode == 2:            
            if num_one_float or num_two_float: 
                if oper == '+':
                    tmp = float(one)+float(two)
                elif oper == '-':
                    tmp = float(one)-float(two)
                elif oper == '*':
                    tmp = float(one)*float(two)
                elif oper == '/':
                    if two != '0':
                        tmp = float(one)/float(two)
                    else:
                        tmp = None
                if tmp != None:
                    calc_reset_full()
                    one, two, num_one_float, num_two_float, mode, oper = calc_data
                    lcd_value = str(tmp)
                    one = lcd_value
                    calc_data = one, two, True, num_two_float, mode, oper
                else:
                    lcd_value = 'Error Zero'
            else:
                if oper == '+':
                    tmp = int(one)+int(two)
                elif oper == '-':
                    tmp = int(one)-int(two)
                elif oper == '*':
                    tmp = int(one)*int(two)
                elif oper == '/':
                    if two != '0':
                        if int(one)%int(two) == 0:
                            tmp = int(int(one)/int(two))
                        else:
                            tmp = float(one)/float(two)
                            num_one_float = True
                    else:
                        tmp = None
                if tmp != None:
                    tmp_float = num_one_float
                    calc_reset_full()
                    one, two, num_one_float, num_two_float, mode, oper = calc_data
                    lcd_value = str(tmp)
                    one = lcd_value
                    calc_data = one, two, tmp_float, num_two_float, mode, oper
                else:
                    lcd_value = 'Error Zero'
        
# Функция onclick - при нажатии кнопки мыши создаем список с параметрами: состояние нажатия
# True - нажата, False - сброшено. В программе если будет отработана проверка координат нажатия,
# выполнится необходимая обработка и первый параметр сбросит в False 
def onclick(x, y):
    global buff 
    buff = [True, x, y]

canvas.set_onclick(onclick)

# А это ребята основная программа :)
while True:
    listering()
    canvas.clear()
    create_object()
    canvas.draw()
