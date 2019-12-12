from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
import scipy.stats as stats
import math
import numpy as np


def main():
    with open('data.txt') as f:
        data = np.array([float(i.strip()) for i in f.readlines()])
        data /= np.max(np.abs(data), axis=0)

    model = GaussianMixture(n_components=2)
    model.fit(np.reshape(data, newshape=(-1, 1)))

    # Draw histogram and GMM
    num_bins = 8
    fig = plt.figure(1)
    _, _, patches = plt.hist(data, bins=num_bins, density=True)
    patches[0].set_facecolor('#548235')
    patches[1].set_facecolor('#a9d18f')
    patches[2].set_facecolor('#c5e0b4')
    patches[3].set_facecolor('#e2f0d9')
    patches[4].set_facecolor('#bdd7ee')
    patches[5].set_facecolor('#9dc3e6')
    patches[6].set_facecolor('#2e74b6')
    patches[7].set_facecolor('#1f4d79')
    plt.title('Frequency Distribution and Generated GMM Distribution')
    plt.xlabel('NMDAR / (NMDAR + AMPAR)')
    plt.ylabel('Density')

    draw_gmm(model, 0.2, 1.2, 5000)
    plt.savefig('gmm.png')

    # Draw separate normal distributions
    plt.figure(2)
    mu_1, sigma_1 = get_mu_and_sigma(model, 1)
    mu_2, sigma_2 = get_mu_and_sigma(model, 2)
    draw_normal_distribution(mu_1, sigma_1)
    draw_normal_distribution(mu_2, sigma_2)
    plt.title('Separate Gaussian Distributions')
    plt.xlabel('NMDAR / (NMDAR + AMPAR)')
    plt.ylabel('Density')
    plt.savefig('separate-gaussian.png')


def draw_gmm(model, lower_bound, upper_bound, num_points):
    gmm_x = np.linspace(lower_bound, upper_bound, num_points)
    gmm_y_sum = np.full_like(gmm_x, fill_value=0, dtype=np.float32)
    for m, c, w in zip(model.means_.ravel(), model.covariances_.ravel(), model.weights_.ravel()):
        gauss = gauss_function(x=gmm_x, amp=1, x0=m, sigma=np.sqrt(c))
        gmm_y_sum += gauss / np.trapz(gauss, gmm_x) * w

    plt.plot(gmm_x, gmm_y_sum, color="black", lw=4, label="GMM", linestyle="dashed")
    plt.legend()


def gauss_function(x, amp, x0, sigma):
    return amp * np.exp(-(x - x0) ** 2. / (2. * sigma ** 2.))


def get_mu_and_sigma(model, num_components):
    num_components -= 1
    mu = model.means_[num_components][0]
    sigma = math.sqrt(model.covariances_[num_components][0][0])
    return mu, sigma


def draw_normal_distribution(mu, sigma):
    x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
    plt.plot(x, stats.norm.pdf(x, mu, sigma) / 2)


if __name__ == '__main__':
    main()
