# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from typing import List, Dict
import logging

from docutils.parsers.rst.roles import role

logging.basicConfig(level=logging.INFO)


class Contributor():

	def __init__(self, index, name):
		self.index = index
		self.name = name
		self.skills = {}
		self.available = True

	def addSkill(self, skill_name, skill_value):
		self.skills[skill_name] = skill_value

	def setAvailable(self, isAvailBool):
		self.available = isAvailBool

	def isAvailable(self):
		return self.available


class Role():
	def __init__(self, role_skill_name, role_skill_level):
		self.role_skill_name = role_skill_name
		self.role_skill_level = role_skill_level


class Project():

	def __init__(self, index, name, days_needed, score, best_before_day):
		self.index = index
		self.name = name
		self.days_needed = days_needed
		self.score = score
		self.best_before_day = best_before_day
		self.roles = {}
		self.assignee = []
		self.appetite = best_before_day

	def addRoles(self, index, role: Role):
		self.roles[index] = role

	def completeProject(self):
		[ass.setAvailable(True) for ass in self.assignee]

	def updateAppetite(self, t):
		self.appetite = self.best_before_day - t


def parse_input(letter):
	filenames = ['data/a.txt',
				 'data/b.txt',
				 'data/c.txt',
				 'data/d.txt',
				 'data/e.txt',
				 'data/f.txt']

	int_to_letter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'f', 5: 'g'}
	letter_to_int = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5}

	f = open(filenames[letter_to_int[letter]])
	# Parse input file
	print('Reading first line')
	line = f.readline()
	C = int(line.split(' ')[0])
	P = int(line.split(' ')[1])

	num_contributors = C
	num_projets = P

	print('num_contributors ' + str(num_contributors))

	contributors = []
	projects = []
	skills = {}

	for c in range(C):
		line = f.readline()
		lineSplit = line.split(' ')
		name = lineSplit[0]
		contributor = Contributor(c, name)
		num_skills = int(lineSplit[1])
		for sk in range(num_skills):
			line = f.readline()
			lineSplit = line.split(' ')
			skill_name = lineSplit[0]
			skill_value = int(lineSplit[1])
			contributor.addSkill(skill_name, skill_value)
			if skill_name in skills:
				skills[skill_name].append(contributor)
			else:
				skills[skill_name] = [contributor]
		contributors.append(contributor)

	for p in range(P):
		line = f.readline()
		lineSplit = line.split(' ')
		name = lineSplit[0]
		days_needed = int(lineSplit[1])
		score = int(lineSplit[2])
		best_before_day = int(lineSplit[3])
		num_roles = int(lineSplit[4])
		project = Project(p, name, days_needed, score, best_before_day)
		for nr in range(num_roles):
			line = f.readline()
			lineSplit = line.split(' ')
			skill_name = lineSplit[0]
			skill_level = int(lineSplit[1])
			project.addRoles(nr, Role(skill_name, skill_level))
		projects.append(project)

	return contributors, projects, skills


class Evaluator:
	def __init__(self, projects: List[Project], contributors: List[Contributor], sortProject: bool,
				 skills_contributors_map: Dict[str, List[Contributor]]):
		if sortProject:
			# To sort the list in place...
			projects.sort(key=lambda x: x.appetite, reverse=False)
		self.projects = projects
		self.contributors = contributors
		self.t = 0
		self.in_progress_projects = {}
		self.completed_projects: List[Project] = []
		self.sortProject = sortProject
		self.score = 0
		self.skills_contributors_map = skills_contributors_map
		self.total_projects = len(projects)
		self.projects_added = 0

	def isMentorAvailable(self, candidates: Dict[str, Contributor], role: Role, project: Project,
						  checkProject=False) -> bool:
		role_skill_name = role.role_skill_name
		role_skill_level = role.role_skill_level
		# First search in already assigned candidates
		for rsn, candidate in candidates.items():
			if candidate is not None and candidate.skills.get(role_skill_name, 0) >= role_skill_level:
				return True
		# Then try to remove one candidate
		if checkProject:
			for index, candidate in candidates.items():
				if candidate is not None:
					role_skill_name_2 = project.roles[index].role_skill_name
					role_skill_level_2 = project.roles[index].role_skill_level
					for contributor in self.skills_contributors_map.get(role_skill_name_2, []):
						if contributor.isAvailable() and contributor is not candidate and contributor.skills.get(
							role_skill_name_2, 0) >= role_skill_level_2 and contributor.skills.get(
							role_skill_name, 0) >= role_skill_level:
							candidates[index] = contributor
							return True

		return False

	def setContributorsToProject(self, project: Project, contributors: Dict[str, Contributor]):
		[ass.setAvailable(False) for ass in contributors.values()]
		for index, role in project.roles.items():
			role_skill_name = role.role_skill_name
			role_skill_level = role.role_skill_level
			project.assignee.append(contributors[index])
			current_skill_level = contributors[index].skills.get(role_skill_name, 0)
			if current_skill_level == role_skill_level or current_skill_level == (role_skill_level - 1):
				contributors[index].skills[role_skill_name] = current_skill_level + 1

	def is_satisfiable(self, project: Project):
		candidates = {}
		count = 0
		num_roles = len(project.roles)
		for index, role in project.roles.items():
			role_skill_name = role.role_skill_name
			role_skill_level = role.role_skill_level
			candidates[index] = None
			for contributor in self.skills_contributors_map.get(role_skill_name, []):
				if contributor.isAvailable() and contributor not in candidates.values():
					if contributor.skills.get(role_skill_name, 0) >= role_skill_level:
						candidates[index] = contributor
						count += 1
						break
					# Basic mentorship
					elif contributor.skills.get(role_skill_name, 0) == (role_skill_level - 1):
						if self.isMentorAvailable(candidates, role, project):
							candidates[index] = contributor
							count += 1
							break

		while count != num_roles:
			isAtLeastOneNewContributorAdded = False
			for index, candidate in candidates.items():
				role_skill_name = project.roles[index].role_skill_name
				role_skill_level = project.roles[index].role_skill_level
				if candidate is None:
					if self.isMentorAvailable(candidates, project.roles[index], project, True):
						for contributor in self.skills_contributors_map.get(role_skill_name, []):
							if contributor.isAvailable() and contributor not in candidates.values() and contributor.skills.get(
									role_skill_name, 0) == (role_skill_level - 1):
								candidates[index] = contributor
								count += 1
								isAtLeastOneNewContributorAdded = True
								break

			if not isAtLeastOneNewContributorAdded:
				# No contributor could be added -> project unfeasible now
				return False

		self.setContributorsToProject(project, candidates)
		return True

	def pickNextProject(self) -> Project:
		# Return project with contributors
		for project in self.projects:
			if project.score - (self.t + project.days_needed - project.best_before_day) < 0:
				# if it will never give points from now on, remove from list
				self.projects.remove(project)
				continue
			if self.is_satisfiable(project):
				# logging.info("Project picked: %s", project.name)
				# Project added, remove from pool of pickable
				self.projects.remove(project)
				return project

	def loop(self):
		last_percentage = 0
		while (True):
			logging.debug("Loop")
			nextProject = self.pickNextProject()
			# if nextProject is not None and len(self.in_progress_projects) < 20:

			# Select a project until is possible
			if nextProject is not None:
				self.projects_added += 1
				percentage_of_projects_added = int(self.projects_added * 100 / self.total_projects)
				if percentage_of_projects_added >= last_percentage:
					print(str(percentage_of_projects_added) + '%')
					# let's print something every 5% of projects
					last_percentage += 5
				# save time it ends
				time_when_ends = self.t + nextProject.days_needed
				self.in_progress_projects[nextProject] = time_when_ends

			# When no other project can be started, move at the time the shortest ones end
			elif self.in_progress_projects != {}:
				self.t = min(self.in_progress_projects.values())
				projects_just_completed = [k for k, v in self.in_progress_projects.items() if v == self.t]

				for p in projects_just_completed:
					self.score += p.score - max(0, (self.t - p.best_before_day))
				self.completed_projects.extend(projects_just_completed)
				[k.completeProject() for k in projects_just_completed]
				[self.in_progress_projects.pop(project, None) for project in projects_just_completed]
			# remove ended project and free contributors and update skills

			# # Update appetite
			# if self.sortProject:
			# 	[p.updateAppetite(self.t) for p in self.projects]
			# 	self.projects.sort(key=lambda x: x.appetite, reverse=False)

			# If no project can be added and no one is ongoing, finish
			else:
				print('Score: ' + str(self.score))
				break


def write_output(letter, completed_projects):
	filename = 'data/out/' + letter + '.txt'
	with open(filename, 'w') as out:
		print(str(len(completed_projects)), file=out)
		for p in completed_projects:
			print(p.name, file=out)
			print(" ".join([x.name for x in p.assignee]), file=out)


if __name__ == '__main__':
	# letters = ['a', 'b', 'c', 'd', 'e', 'f']
	letters = ['b']
	for letter in letters:
		contributors, projects, skills = parse_input(letter)
		sortProject = True
		evaluator = Evaluator(projects, contributors, sortProject, skills)
		evaluator.loop()

		write_output(letter, evaluator.completed_projects)
