import time
from Astar import *
import copy

class W_Robot:
    def __init__(self,capacity,packing_station,packing_station_ind,current_point,property=None):
        self.capcity = capacity
        self.property =property
        self.is_work = False#로봇이 일하고 있는가?
        self.home_packing_station = packing_station#시작하고 돌아오는 패킹지점
        self.packing_station_ind = packing_station_ind#occupy map에서 패킹지점의 인덱스
        self.current_point = current_point#occupy_grid map에서의 현재 로봇 위치
        self.is_ghost = True#로봇이 다른 로봇을 통과하는가?
        self.picking_point = []#로봇에게 부여된 피킹지점들
        self.last_ind = 0 #이미 들린 마지막 장소의 인덱스(패킹지점 포함) ex) 0(패킹지점) - 1(첫 번째 선반) -
        self.prev_point = self.home_packing_station#로봇의 현재 위치 이전의 좌표
        self.goal_point = []#현재 로봇이 향하는 목표점
        self.occupy_map =None
        self.route =[]
        self.route_maxind =6
        self.full_route =[]
        #Astar를 추가하였습니다.
        self.astar_route = []
        self.astar_ind = 0


        ## 시물레이션 비교를 위해서 추가한 코드입니다.
        self.route_step =0#한 시물레이션동안에 알고리즘에 대한 이동시간
        self.algorithm_time = 0#한 시물레이션동안에 알고리즘수행시간

    def astar_move(self):
        if self.is_work:
            # 알고리즘 적용
            blocked_flag = True
            find_goal = False
            move_control = [[0,1],[1,0],[0,-1],[-1,0],[1,1],[1,-1],[-1,-1],[-1,1]]
            if len(self.astar_route) == 1:#이미 도착했다면(처음시작점과 도착점이 같아버림)
                if self.chanage_goal_astar():#다음위치로 가버립니다.
                    self.is_work = False
            next_pos = self.astar_route[self.astar_ind]#astar_ind를 기반으로 하여 바뀐 위치 아직 실제 로봇에 적용은 안함.
            self.astar_ind +=1
            # blocked_flag = False#막힌곳이 없을것이다.
            #print(next_pos)
            for control in move_control:
                cand_y = control[0] + next_pos[0]#현재 이동한지점 주변에 도착했는지 찾습니다.
                cand_x = control[1] + next_pos[1]#현재 이동한지점 주변에 도착했는지 찾습니다.
                if self.occupy_map[cand_y][cand_x] == self.picking_point[self.last_ind+1]: # 주변에 사변이 해당로봇이 가야하는 지점과 목표 값이 같다면,
                    find_goal = True

            self.prev_point = [self.current_point[0], self.current_point[1]]
            #현재 경로를 갱신하는부분
            self.current_point[0] = next_pos[0]
            self.current_point[1] = next_pos[1]
            self.route_step +=1
            if find_goal:# 골에 도착했다면 목표위치를 바꾼다.
                if self.chanage_goal_astar():
                    self.is_work = False

            #최근경로를 저장하는부분
            if len(self.route)<= self.route_maxind:
                route_x = self.current_point[1]
                route_y = self.current_point[0]
                self.route.append([route_y,route_x])
            else :
                self.route.pop(0)
                route_x = self.current_point[1]
                route_y = self.current_point[0]
                self.route.append([route_y, route_x])

            route_x = self.current_point[1]
            route_y = self.current_point[0]
            self.full_route.append([route_y, route_x])

    def chanage_goal_astar(self):#패킹지점인지 확인한다.
        last_index = len(self.picking_point)-1
        if self.last_ind != last_index-1 :#last_ind가 패킹 선반 다돌고, 마지막 패킹지점으로 오지 않았다면(last_ind가 마지막에서 한 개 전이어야함.)
            if self.last_ind <last_index-2:
                goal_candidate = self.shelf_grid_list[self.last_ind+1]#해당 선반이 포함하고 있는 모든 점을 찾는다.
                min_dis = 1000
                min_ind = -1
                for i, point in enumerate(goal_candidate):
                    dis = (point[0] - self.current_point[0]) * (point[0] - self.current_point[0]) + (
                                point[1] - self.current_point[1]) * (point[1] - self.current_point[1])
                    if dis < min_dis:
                        min_ind = i
                        min_dis = dis
                self.goal_point = goal_candidate[min_ind]  # 로봇과 가까운 지점.
                self.astar_ind = 0
                self.astar_route = astar_path(self.occupy_map, self.current_point, self.goal_point)
            else :
                self.goal_point = self.home_packing_station#골 후보를 그냥 패킹지점으로 준다.
                self.astar_ind = 0
                self.astar_route = astar_path(self.occupy_map, self.current_point, self.goal_point)
            self.last_ind +=1
            return False
        else :#last_ind가 패킹 선반 다돌고, 마지막 패킹지점으로 왔다면
            self.last_ind =0
            self.route = []
            self.full_route = []
            return True

    def assign_work_astar(self, picking_point, shelf_grid_list,occupy_map):
        self.picking_point = [self.packing_station_ind] + picking_point + [self.packing_station_ind]
        self.shelf_grid_list = shelf_grid_list
        self.is_work = True
        goal_candidate = self.shelf_grid_list[self.last_ind]  # 해당 선반이 포함하고 있는 모든 점을 찾는다.
        min_dis = 1000
        min_ind = -1
        for i, point in enumerate(goal_candidate):
            dis = (point[0] - self.current_point[0]) * (point[0] - self.current_point[0]) + (
                    point[1] - self.current_point[1]) * (point[1] - self.current_point[1])
            if dis < min_dis:
                min_ind = i
                min_dis = dis
        self.goal_point = goal_candidate[min_ind]  # 로봇과 가까운 목표 선반 포인트를 찾는다.
        self.occupy_map = occupy_map
        self.astar_route = astar_path(self.occupy_map, self.current_point, self.goal_point)
        self.astar_ind = 0
        self.full_route = []