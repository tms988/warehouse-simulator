

def online_order_batch(orders, item_position, init_batch_size, max_batch_size, current_robot_batch):
    '''
    ********************************************************************
    ******************************Input*********************************
    ********************************************************************
    -------------------------------------------------------------------
     orders,
        - 자료형 : 2차원 list,
        - 설명 : 1차원 list 자료형의 새로들어온 order를 가지고 잇음.
                각각의 order는 int 자료형의 item(물품)을 가지고 있다.
     ex) 1,2,3 item들을 가진 order와 2,3,4 item들을 가진 order가 있을때
     orders  -> [[1,2,3], [2,3,4]]
     -------------------------------------------------------------------
     item_position,
        - 자료형 : 2차원 list,
        - 설명 : 1차원 list 자료형으로 아이템들의 위치 좌표(x, y)를 가지고 있다.
                각 아이템에 위치는 다음과같이 찾을 수 있다.
     ex) k item의 위치를 찾는다면
     k item의 위치(좌표) -> item_position[k] , k item의 x 좌표 -> item_position[k][0], k item의 y 좌표 -> item_position[k][1]
     --------------------------------------------------------------------
    init_batch_size,
        - 자료형 : int
        - 설명 : 초기 batch가 가질 수 있는 최대 item 수
    ---------------------------------------------------------------------
    max_batch_size,
        - 자료형 : int
        - 설명 : online order batch간에 로봇이 가질 수 있는 최대 item 수
    ---------------------------------------------------------------------
    current_robot_batch,
        - 자료형 : 2차원 list
        - 설명 : online order batch간에 로봇들이 현재 가진 batch
                특정 로봇에게 batch가 할당이 되었다면, 할당된 batch로 채워져있다.
                특정 로봇에게 batch가 할당이 안되있다면,[]로 채워져있다.

    ex) 현재 4개의 로봇중에서 , 0번과 2번에게만 batch([1,2,3]과 [2,4,5])가 각각 할당되어있다면
    current_robot_batch =  [[1,2,3],[],[2,4,5],[]]
    ---------------------------------------------------------------------
    ********************************************************************
    ******************************Output********************************
    ********************************************************************
    return_robot_batch,
        - 자료형 : 2차원 list,
        - 설명 : 인자로 준 orders에서 batch로 묶은 결과를 로봇에게 할당한 결과
    ---------------------------------------------------------------------
    remain_order,
        - 자료형 : 2차원 list,
        - 설명 : 인자로 준 orders에서 batch로 묶은 결과를 로봇에게 할당하고 남은 order의 집합
    ---------------------------------------------------------------------

    ex) A = [1, 2, 3] / B = [4, 5, 6]  / C = [1, 2, 4] / D = [1, 7, 5] 을 가지는 order에 대해서
    init_batch_size가 6이고, max_batch_size = 12라면, current_robot_batch를 고려하여 다음과 같이 만든다.

    (입력)
    orders = [[1, 2, 3],[4, 5, 6],[1, 2, 4],[1, 7, 5]]
    init_batch_size = 6
    max_batch_size = 12
    current_robot_batch =  [[1,2,3],[],[2,4,5],[]]



    (출력)
    return_robot_batch =  [[1, 2, 3, 1, 2, 3, 1, 2, 4], [], [2, 4, 5, 4, 5, 6],[]]
    remain_order = [[1, 7, 5]]

    '''
    return_robot_batch = []
    remain_order = []

    #todo

    return return_robot_batch, remain_order