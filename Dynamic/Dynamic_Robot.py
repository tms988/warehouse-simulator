import time
from Astar import *
import copy

class W_Robot:
    def __init__(self,capacity,packing_station,packing_station_ind,current_point,property=None):
        self.capcity = capacity
        self.property =property
        self.home_packing_station = packing_station#시작하고 돌아오는 패킹지점
        self.packing_station_ind = packing_station_ind#occupy map에서 패킹지점의 인덱스
        self.current_point = current_point#occupy_grid map에서의 현재 로봇 위치
        self.is_ghost = True#로봇이 다른 로봇을 통과하는가?
        self.picking_point = []#로봇에게 부여된 피킹지점들
        self.last_picking_shelf_index = 0 #이미 들린 마지막 장소의 인덱스(패킹지점 포함) ex) 0(패킹지점) - 1(첫 번째 선반) -
        self.prev_point = self.home_packing_station#로봇의 현재 위치 이전의 좌표
        self.goal_point = []#현재 로봇이 향하는 목표점
        self.occupy_map =None

        #Astar를 추가하였습니다.
        self.astar_route = []
        self.astar_ind = 0

        #online이라서 이미 간노드르 초기화합니다.
        self.already_gone_node = []

        #패킹지점에 도달하면 flag가 True가 됩니다.
        self.packing_point_arrive = False

    def astar_move(self):
        find_goal = False

        #로봇이 앞으로 갈 지점을 얻습니다.
        next_pos = self.get_next_robot_pos()

        #다음 주변 점을 확인해서, 목표지점이 있는지 확인합니다.
        find_goal = self.observe_8_neigh(next_pos)

        #로봇의 포즈를 업데이트합니다.
        self.update_robot_pos(next_pos)

        # 골에 도착했다면 목표위치를 바꾼다.
        if find_goal:
            self.chanage_goal_astar()

    def chanage_goal_astar(self):# 패킹지점인지 확인한다.
        last_packing_index = len(self.picking_point)-1#마지막 패킹 지점의 인덱스

        if self.last_picking_shelf_index != last_packing_index -1:#last_ind가 피킹 선반들을 다돌고, 마지막 패킹지점으로 오지 않았다면(last_ind가 마지막에서 한 개 전이어야함.)
            self.set_goal_point(last_packing_index)# 패킹 지점을 목적지로 정할지, 피킹 지점을 목적지로 정할지 고릅니다.
            self.robot_goal_point_reset()#로봇의 골지점을 리셋하고, astar경로를 다시구합니다.
            return False

        else :#last_ind가 피킹 선반 다돌고, 마지막 패킹지점으로 왔다면(last ind가 마지막으로 피킹한지점이라면
            self.already_gone_node = []
            self.last_picking_shelf_index =0
            self.packing_point_arrive = True
            return True

    def assign_work_astar(self, picking_point, shelf_grid_list,occupy_map):
        self.picking_point = [-1] + picking_point + [self.packing_station_ind]
        self.shelf_grid_list = shelf_grid_list#노드로 여겨지는 선반들에 대한 임시 목표지점들을 선택한다.(현재 위치는 포함 x)
        goal_candidate = self.shelf_grid_list[self.last_picking_shelf_index]  # 해당 선반이 포함하고 있는 모든 점을 찾는다.
        min_dis = 1000
        min_ind = -1

        for i, point in enumerate(goal_candidate):
            dis = (point[0] - self.current_point[0]) * (point[0] - self.current_point[0]) + (
                    point[1] - self.current_point[1]) * (point[1] - self.current_point[1])
            if dis < min_dis:
                min_ind = i
                min_dis = dis

        self.goal_point = goal_candidate[min_ind]  # 로봇과 가까운 목표 선반 포인트를 찾는다.
        self.occupy_map = occupy_map #occupy map을 등록한다.
        self.astar_route = astar_path(self.occupy_map, self.current_point, self.goal_point)#목표지점에 대한 경로를 생성한다.
        self.astar_ind = 0

    def set_goal_point(self,last_packing_index):
        if self.last_picking_shelf_index < last_packing_index - 2:  # 아직 피킹지점의 마지막이 아니라면
            goal_candidate = self.shelf_grid_list[self.last_picking_shelf_index + 1]  # 해당 선반이 포함하고 있는 모든 점을 찾는다.
            min_dis = 1000
            min_ind = -1
            for i, point in enumerate(goal_candidate):
                dis = (point[0] - self.current_point[0]) * (point[0] - self.current_point[0]) + (
                        point[1] - self.current_point[1]) * (point[1] - self.current_point[1])
                if dis < min_dis:
                    min_ind = i
                    min_dis = dis
            self.goal_point = goal_candidate[min_ind]  # 로봇과 가까운 지점.
        else:
            self.goal_point = self.home_packing_station  # 골 후보를 그냥 패킹지점으로 준다.


    def robot_goal_point_reset(self):
        self.astar_ind = 0  # 이동지점 초기화
        self.astar_route = astar_path(self.occupy_map, self.current_point, self.goal_point)
        self.already_gone_node.append(self.picking_point[self.last_picking_shelf_index + 1])#이미 간 노드를 추가합니다.
        self.last_picking_shelf_index += 1  # 초기에 0에서 시작함.

    def get_next_robot_pos(self):
        robot_point = self.astar_route[self.astar_ind]  # astar_ind를 기반으로 하여 바뀐 위치 아직 실제 로봇에 적용은 안함.
        self.astar_ind += 1
        return robot_point

    def observe_8_neigh(self,next_pos):
        observe_8 = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, -1], [-1, 1]]
        for view in observe_8:
            cand_y = view[0] + next_pos[0]  # 현재 이동할 지점 주변에 도착했는지 찾습니다.
            cand_x = view[1] + next_pos[1]  # 현재 이동할 지점 주변에 도착했는지 찾습니다.
            if self.picking_point[self.last_picking_shelf_index + 1] > 20000:
                if self.occupy_map[cand_y][cand_x] == (self.picking_point[
                                                           self.last_picking_shelf_index+ 1]):  # 주변에 사변이 해당로봇이 가야하는 지점과 목표 값이 같다면,
                    return True
            else :
                if self.occupy_map[cand_y][cand_x] == (self.picking_point[
                    self.last_picking_shelf_index + 1]+1):  # 주변에 사변이 해당로봇이 가야하는 지점과 목표 값이 같다면,
                    return True
        return False

    def update_robot_pos(self,next_pos):
        self.prev_point = [self.current_point[0], self.current_point[1]]
        # 현재 경로를 갱신하는부분
        self.current_point[0] = next_pos[0]
        self.current_point[1] = next_pos[1]


